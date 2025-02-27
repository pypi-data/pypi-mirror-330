"""Agent model implementation"""
import os
import weave
from weave import Model, Prompt
import json
import base64
import magic
from typing import List, Dict, Any, Optional, Union, AsyncGenerator, Tuple
from datetime import datetime, UTC
from pydantic import Field, PrivateAttr
from litellm import acompletion
from tyler.models.thread import Thread
from tyler.models.message import Message
from tyler.models.attachment import Attachment
from tyler.database.memory_store import MemoryThreadStore
from tyler.utils.tool_runner import tool_runner
from enum import Enum
from tyler.utils.logging import get_logger

# Get configured logger
logger = get_logger(__name__)

class StreamUpdate:
    """Update from streaming response"""
    class Type(Enum):
        CONTENT_CHUNK = "content_chunk"      # Partial content from assistant
        ASSISTANT_MESSAGE = "assistant_message"  # Complete assistant message with tool calls
        TOOL_MESSAGE = "tool_message"        # Tool execution result
        COMPLETE = "complete"                # Final thread state and messages
        ERROR = "error"                      # Error during processing
        
    def __init__(self, type: Type, data: Any):
        self.type = type
        self.data = data

class AgentPrompt(Prompt):
    system_template: str = Field(default="""You are {name}, an LLM agent with a specific purpose that can converse with users, answer questions, and when necessary, use tools to perform tasks.

Current date: {current_date}
                                 
Your purpose is: {purpose}

Some are some relevant notes to help you accomplish your purpose:
```
{notes}
```
""")

    @weave.op()
    def system_prompt(self, purpose: str, name: str, notes: str = "") -> str:
        return self.system_template.format(
            current_date=datetime.now().strftime("%Y-%m-%d %A"),
            purpose=purpose,
            name=name,
            notes=notes
        )

class Agent(Model):
    model_name: str = Field(default="gpt-4o")
    temperature: float = Field(default=0.7)
    name: str = Field(default="Tyler")
    purpose: str = Field(default="To be a helpful assistant.")
    notes: str = Field(default="")
    tools: List[Union[str, Dict]] = Field(default_factory=list, description="List of tools available to the agent. Can include built-in tool module names (as strings) and custom tools (as dicts with required 'definition' and 'implementation' keys, and an optional 'attributes' key for tool metadata).")
    max_tool_iterations: int = Field(default=10)
    thread_store: Optional[object] = Field(default_factory=MemoryThreadStore, description="Thread storage implementation. Uses in-memory storage by default.")
    
    _prompt: AgentPrompt = PrivateAttr(default_factory=AgentPrompt)
    _iteration_count: int = PrivateAttr(default=0)
    _processed_tools: List[Dict] = PrivateAttr(default_factory=list)

    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "allow"
    }

    def __init__(self, **data):
        super().__init__(**data)
        
        # Load tools
        self._processed_tools = []
        for tool in self.tools:
            if isinstance(tool, str):
                # Load built-in tool module
                loaded_tools = tool_runner.load_tool_module(tool)
                if loaded_tools:
                    self._processed_tools.extend(loaded_tools)
            elif isinstance(tool, dict):
                # Add custom tool
                if 'definition' not in tool or 'implementation' not in tool:
                    raise ValueError("Custom tools must have 'definition' and 'implementation' keys")
                    
                # Register the tool
                tool_name = tool['definition']['function']['name']
                tool_runner.register_tool(
                    name=tool_name,
                    implementation=tool['implementation'],
                    definition=tool['definition']['function']
                )
                
                # Register any tool attributes
                if 'attributes' in tool:
                    tool_runner.register_tool_attributes(tool_name, tool['attributes'])
                    
                self._processed_tools.append(tool['definition'])
            else:
                raise ValueError(f"Invalid tool type: {type(tool)}")

    @weave.op()
    def _normalize_tool_call(self, tool_call):
        """Convert a tool_call dict to an object with attributes so it can be used by tool_runner."""
        if isinstance(tool_call, dict):
            from types import SimpleNamespace
            function_data = tool_call.get("function", {})
            normalized_function = SimpleNamespace(**function_data)
            normalized = SimpleNamespace(
                id=tool_call.get("id"),
                type=tool_call.get("type", "function"),
                function=normalized_function
            )
            return normalized
        return tool_call

    @weave.op()
    async def _handle_tool_execution(self, tool_call) -> dict:
        """
        Execute a single tool call and format the result message
        
        Args:
            tool_call: The tool call object from the model response
        
        Returns:
            dict: Formatted tool result message
        """
        normalized_tool_call = self._normalize_tool_call(tool_call)
        # If the arguments string is empty or only whitespace, replace it with '{}'
        if not normalized_tool_call.function.arguments or normalized_tool_call.function.arguments.strip() == "":
            normalized_tool_call.function.arguments = "{}"
        
        return await tool_runner.execute_tool_call(normalized_tool_call)

    @weave.op()
    async def _process_streaming_chunks(self, chunks) -> Tuple[str, str, List[Dict], Dict]:
        """Process streaming chunks from the LLM.
        
        Args:
            chunks: Async generator of completion chunks
        
        Returns:
            Tuple[str, str, List[Dict], Dict]: A tuple containing:
                - pre_tool_content: aggregated content prior to any tool call
                - post_tool_content: aggregated content after the first tool call
                - tool_calls: list of tool calls encountered (from the first chunk with tool calls)
                - usage_metrics: taken from the final chunk
        """
        if chunks is None or not hasattr(chunks, '__aiter__'):
            raise TypeError(f"'async for' requires an object with __aiter__ method, got {type(chunks).__name__}")

        pre_tool_content = ""
        post_tool_content = ""
        tool_calls = []
        encountered_tool = False
        final_chunk = None
        current_tool_call = None

        async for chunk in chunks:
            final_chunk = chunk
            delta = chunk.choices[0].delta
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
                if not encountered_tool:
                    # First time encountering tool calls, record them
                    for tc in delta.tool_calls:
                        if isinstance(tc, dict):
                            normalized = tc
                        else:
                            normalized = {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                        tool_calls.append(normalized)
                        current_tool_call = normalized
                    encountered_tool = True
                else:
                    # Already encountered tool calls; append continuation chunks' arguments
                    for tc in delta.tool_calls:
                        if current_tool_call is not None and isinstance(tc, dict) and not tc.get("id"):
                            current_tool_call["function"]["arguments"] += tc.get("function", {}).get("arguments", "")
                        elif current_tool_call is not None and not hasattr(tc, 'id'):
                            current_tool_call["function"]["arguments"] += getattr(tc.function, 'arguments', "")
                    # After processing continuation chunks, normalize the aggregated JSON string
                    if current_tool_call is not None:
                        agg = current_tool_call["function"]["arguments"].strip()
                        if not agg.startswith("{"):
                            agg = "{" + agg
                        if not agg.endswith("}"):
                            agg = agg + "}"
                        current_tool_call["function"]["arguments"] = agg
                if hasattr(delta, 'content') and delta.content is not None:
                    post_tool_content += delta.content
            else:
                if not encountered_tool:
                    if hasattr(delta, 'content') and delta.content is not None:
                        pre_tool_content += delta.content
                else:
                    if hasattr(delta, 'content') and delta.content is not None:
                        post_tool_content += delta.content

        usage_metrics = {}
        if final_chunk and hasattr(final_chunk, 'usage') and final_chunk.usage:
            usage_metrics = {
                "completion_tokens": final_chunk.usage.completion_tokens,
                "prompt_tokens": final_chunk.usage.prompt_tokens,
                "total_tokens": final_chunk.usage.total_tokens
            }

        return pre_tool_content, post_tool_content, tool_calls, usage_metrics

    @weave.op()
    async def _process_message_files(self, message: Message) -> None:
        """Process any files attached to the message"""
        for attachment in message.attachments:
            try:
                # Get content as bytes
                content = await attachment.get_content_bytes()
                
                # Check if it's an image and set mime_type first
                mime_type = magic.from_buffer(content, mime=True)
                attachment.mime_type = mime_type
                
                if mime_type.startswith('image/'):
                    # Store the image content in the attachment
                    attachment.processed_content = {
                        "type": "image",
                        "content": base64.b64encode(content).decode('utf-8'),
                        "mime_type": mime_type
                    }
                elif mime_type.startswith('audio/'):
                    # Special handling for audio files - just store the MIME type
                    attachment.processed_content = {
                        "type": "audio",
                        "mime_type": mime_type
                    }
                else:
                    # Use read-file tool for text files and PDFs
                    await attachment.ensure_stored()
                    result = await tool_runner.run_tool_async(
                        "read-file",
                        {
                            "file_url": attachment.storage_path,
                            "mime_type": mime_type
                        }
                    )
                    attachment.processed_content = result
                    
            except Exception as e:
                attachment.processed_content = {"error": f"Failed to process file: {str(e)}"}
                
            # Ensure the attachment is stored
            await attachment.ensure_stored()
        
        # After processing all attachments, update the message content if there are images
        image_attachments = [
            att for att in message.attachments 
            if att.processed_content and att.processed_content.get("type") == "image"
        ]
        
        # Don't modify the content - it should stay as text only
        # The Message.to_chat_completion_message() method will handle creating the multimodal format
    
    @weave.op()
    async def _get_completion(self, **completion_params) -> Any:
        """Get a completion from the LLM with weave tracing.
        
        Returns:
            Any: The completion response. When called with .call(), also returns weave_call info.
            If streaming is enabled, returns an async generator of completion chunks.
        """
        # Call completion directly first to get the response
        response = await acompletion(**completion_params)
        return response
    
    @weave.op()
    async def step(self, thread: Thread, stream: bool = False) -> Tuple[Any, Dict]:
        """Execute a single step of the agent's processing.
        
        A step consists of:
        1. Getting a completion from the LLM
        2. Collecting metrics about the completion
        3. Processing any tool calls if present
        
        Args:
            thread: The thread to process
            stream: Whether to stream the response. Defaults to False.
            
        Returns:
            Tuple[Any, Dict]: The completion response and metrics.
        """
        completion_params = {
            "model": self.model_name,
            "messages": thread.get_messages_for_chat_completion(),
            "temperature": self.temperature,
            "stream": stream
        }
        
        if len(self._processed_tools) > 0:
            completion_params["tools"] = self._processed_tools
        
        # Track API call time
        api_start_time = datetime.now(UTC)
        
        try:
            # Get completion with weave call tracking
            response, call = await self._get_completion.call(self, **completion_params)
            
            # Create metrics dict with essential data
            metrics = {
                "model": self.model_name,  # Use model_name since streaming responses don't include model
                "timing": {
                    "started_at": api_start_time.isoformat(),
                    "ended_at": datetime.now(UTC).isoformat(),
                    "latency": (datetime.now(UTC) - api_start_time).total_seconds() * 1000
                }
            }

            # Add weave-specific metrics if available
            try:
                if hasattr(call, 'id') and call.id:
                    metrics["weave_call"] = {
                        "id": str(call.id),
                        "ui_url": str(call.ui_url)
                    }
            except (AttributeError, ValueError):
                pass
            
            # Get usage metrics if available
            if hasattr(response, 'usage'):
                metrics["usage"] = {
                    "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "total_tokens": getattr(response.usage, "total_tokens", 0)
                }
                    
            return response, metrics
        except Exception as e:
            error_text = f"I encountered an error: {str(e)}"
            error_msg = Message(role='assistant', content=error_text)
            error_msg.metrics = {"error": str(e)}
            thread.add_message(error_msg)
            return thread, [error_msg]

    @weave.op()
    async def _get_thread(self, thread_or_id: Union[str, Thread]) -> Thread:
        """Get thread object from ID or return the thread object directly."""
        if isinstance(thread_or_id, str):
            if not self.thread_store:
                raise ValueError("Thread store is required when passing thread ID")
            thread = await self.thread_store.get(thread_or_id)
            if not thread:
                raise ValueError(f"Thread with ID {thread_or_id} not found")
            return thread
        return thread_or_id

    @weave.op()
    def _serialize_tool_calls(self, tool_calls: Optional[List[Any]]) -> Optional[List[Dict]]:
        """Serialize tool calls to a list of dictionaries.

        Args:
            tool_calls: List of tool calls to serialize, or None

        Returns:
            Optional[List[Dict]]: Serialized tool calls, or None if input is None
        """
        if tool_calls is None:
            return None
            
        serialized = []
        for tool_call in tool_calls:
            if isinstance(tool_call, dict):
                # Ensure ID is present
                if not tool_call.get('id'):
                    continue
                serialized.append(tool_call)
            else:
                # Ensure ID is present
                if not hasattr(tool_call, 'id') or not tool_call.id:
                    continue
                serialized.append({
                    "id": str(tool_call.id),
                    "type": str(tool_call.type),
                    "function": {
                        "name": str(tool_call.function.name),
                        "arguments": str(tool_call.function.arguments)
                    }
                })
        return serialized if serialized else None

    @weave.op()
    async def _process_tool_call(self, tool_call, thread: Thread, new_messages: List[Message]) -> bool:
        """Process a single tool call and return whether to break the iteration."""
        # Get tool name based on tool_call type
        tool_name = tool_call['function']['name'] if isinstance(tool_call, dict) else tool_call.function.name
        
        # Get tool attributes before execution
        tool_attributes = tool_runner.get_tool_attributes(tool_name)

        # Execute the tool
        tool_start_time = datetime.now(UTC)
        try:
            result = await self._handle_tool_execution(tool_call)
        except Exception as e:
            # Handle tool execution error
            result = {
                "name": tool_name,
                "content": f"Error executing tool: {str(e)}"
            }

        # Create tool metrics
        tool_metrics = {
            "timing": {
                "started_at": tool_start_time.isoformat(),
                "ended_at": datetime.now(UTC).isoformat(),
                "latency": (datetime.now(UTC) - tool_start_time).total_seconds() * 1000
            }
        }

        # Create attachments from files if present
        attachments = []
        if result.get("files"):
            for file_info in result["files"]:
                attachment = Attachment(
                    filename=file_info["filename"],
                    content=file_info["content"],
                    mime_type=file_info["mime_type"]
                )
                if "description" in file_info:
                    attachment.processed_content = {
                        "description": file_info["description"]
                    }
                attachments.append(attachment)

        # Add tool result message
        message = Message(
            role="tool",
            content=result["content"],
            name=str(result.get("name", tool_name)),
            tool_call_id=str(tool_call['id'] if isinstance(tool_call, dict) else tool_call.id),
            attributes={"tool_attributes": tool_attributes or {}},
            metrics=tool_metrics,
            attachments=attachments
        )
        thread.add_message(message)
        new_messages.append(message)

        # Check if this is an interrupt tool
        if tool_attributes and tool_attributes.get('type') == 'interrupt':
            return True

        return False

    @weave.op()
    async def _handle_max_iterations(self, thread: Thread, new_messages: List[Message]) -> Tuple[Thread, List[Message]]:
        """Handle the case when max iterations is reached."""
        message = Message(
            role="assistant",
            content="Maximum tool iteration count reached. Stopping further tool calls."
        )
        thread.add_message(message)
        new_messages.append(message)
        if self.thread_store:
            await self.thread_store.save(thread)
        return thread, [m for m in new_messages if m.role != "user"]

    @weave.op()
    async def go(self, thread_or_id: Union[str, Thread], new_messages: Optional[List[Message]] = None) -> Tuple[Thread, List[Message]]:
        """
        Process the next step in the thread by generating a response and handling any tool calls.
        Uses an iterative approach to handle multiple tool calls.
        
        Args:
            thread_or_id (Union[str, Thread]): Either a Thread object or thread ID to process
            new_messages (List[Message], optional): Messages added during this processing round
            
        Returns:
            Tuple[Thread, List[Message]]: The processed thread and list of new non-user messages
            
        Raises:
            ValueError: If thread_or_id is a string and the thread is not found
        """
        # Initialize new messages if not provided
        if new_messages is None:
            new_messages = []
            
        thread = None
        try:
            # Get and initialize thread - let ValueError propagate for thread not found
            try:
                thread = await self._get_thread(thread_or_id)
            except ValueError:
                raise  # Re-raise ValueError for thread not found
            
            system_prompt = self._prompt.system_prompt(self.purpose, self.name, self.notes)
            thread.ensure_system_prompt(system_prompt)
            
            # Check if we've already hit max iterations
            if self._iteration_count >= self.max_tool_iterations:
                return await self._handle_max_iterations(thread, new_messages)
            
            # Process any files in the last user message
            last_message = thread.get_last_message_by_role("user")
            if last_message and last_message.attachments:
                await self._process_message_files(last_message)
                if self.thread_store:
                    await self.thread_store.save(thread)

            # Main iteration loop
            while self._iteration_count < self.max_tool_iterations:
                try:
                    # Get completion and process response
                    response, metrics = await self.step(thread)
                    
                    if not response or not hasattr(response, 'choices') or not response.choices:
                        error_msg = "Failed to get valid response from chat completion"
                        logger.error(error_msg)
                        message = Message(
                            role="assistant",
                            content=f"I encountered an error: {error_msg}. Please try again.",
                            metrics=metrics
                        )
                        thread.add_message(message)
                        new_messages.append(message)
                        break
                    
                    # For non-streaming responses, get content and tool calls directly
                    assistant_message = response.choices[0].message
                    pre_tool = assistant_message.content or ""
                    tool_calls = getattr(assistant_message, 'tool_calls', None)
                    has_tool_calls = tool_calls is not None and len(tool_calls) > 0

                    # Create and add assistant message for pre-tool content if any
                    if pre_tool or has_tool_calls:
                        message = Message(
                            role="assistant",
                            content=pre_tool,
                            tool_calls=self._serialize_tool_calls(tool_calls) if has_tool_calls else None,
                            metrics=metrics
                        )
                        thread.add_message(message)
                        new_messages.append(message)

                    # Process tool calls if any
                    if has_tool_calls:
                        should_break = False
                        for tool_call in tool_calls:
                            if await self._process_tool_call(tool_call, thread, new_messages):
                                should_break = True
                                break
                        if should_break:
                            break
                    
                    # If no tool calls, we are done
                    if not has_tool_calls:
                        break
                        
                    self._iteration_count += 1

                except Exception as e:
                    error_msg = f"Error during chat completion: {str(e)}"
                    logger.error(error_msg)
                    message = Message(
                        role="assistant",
                        content=f"I encountered an error: {error_msg}. Please try again.",
                        metrics={"error": str(e)}
                    )
                    thread.add_message(message)
                    new_messages.append(message)
                    break
                
            # Handle max iterations if needed
            if self._iteration_count >= self.max_tool_iterations:
                message = Message(
                    role="assistant",
                    content="Maximum tool iteration count reached. Stopping further tool calls."
                )
                thread.add_message(message)
                new_messages.append(message)
                
            # Reset iteration count before returning
            self._iteration_count = 0
                
            # Save the final state
            if self.thread_store:
                await self.thread_store.save(thread)
                
            return thread, [m for m in new_messages if m.role != "user"]

        except ValueError:
            # Re-raise ValueError for thread not found
            raise
        except Exception as e:
            error_msg = f"Error processing thread: {str(e)}"
            logger.error(error_msg)
            message = Message(
                role="assistant",
                content=f"I encountered an error: {error_msg}. Please try again.",
                metrics={"error": str(e)}
            )
            
            if isinstance(thread_or_id, Thread):
                # If we were passed a Thread object directly, use it
                thread = thread_or_id
            elif thread is None:
                # If thread creation failed, create a new one
                thread = Thread()
                
            thread.add_message(message)
            if self.thread_store:
                await self.thread_store.save(thread)
            return thread, [message]

    @weave.op()
    async def go_stream(self, thread: Thread) -> AsyncGenerator[StreamUpdate, None]:
        """Process the thread with streaming updates.
        
        Yields:
            StreamUpdate objects containing:
            - Content chunks as they arrive
            - Complete assistant messages with tool calls
            - Tool execution results
            - Final thread state
            - Any errors that occur
        """
        try:
            self._iteration_count = 0
            current_content = []  # Accumulate content chunks
            current_tool_calls = []  # Accumulate tool calls
            current_tool_call = None  # Track current tool call being built
            api_start_time = None  # Track API call start time
            current_weave_call = None  # Track current weave call

            while self._iteration_count < self.max_tool_iterations:
                try:
                    # Get streaming response using step
                    streaming_response, metrics = await self.step(thread, stream=True)
                    
                    if not streaming_response:
                        raise ValueError("No response received from completion call")

                    # Process streaming response
                    async for chunk in streaming_response:
                        if not hasattr(chunk, 'choices') or not chunk.choices:
                            continue

                        delta = chunk.choices[0].delta
                        
                        # Handle content chunks
                        if hasattr(delta, 'content') and delta.content is not None:
                            current_content.append(delta.content)
                            yield StreamUpdate(StreamUpdate.Type.CONTENT_CHUNK, delta.content)
                            
                        # Gather tool calls (don't yield yet)
                        if hasattr(delta, 'tool_calls') and delta.tool_calls:
                            logger.debug(f"Tool call chunk: {delta.tool_calls}")
                            for tool_call in delta.tool_calls:
                                # Log the tool call structure
                                logger.debug(f"Processing tool call: {tool_call}")
                                if isinstance(tool_call, dict):
                                    logger.debug(f"Dict tool call: {tool_call}")
                                else:
                                    logger.debug(f"Object tool call - has id: {hasattr(tool_call, 'id')}, has function: {hasattr(tool_call, 'function')}")
                                    if hasattr(tool_call, 'function'):
                                        logger.debug(f"Function attrs - has name: {hasattr(tool_call.function, 'name')}, has arguments: {hasattr(tool_call.function, 'arguments')}")

                                # Handle both dict and object formats
                                if isinstance(tool_call, dict):
                                    if 'id' in tool_call and tool_call['id']:
                                        # New tool call
                                        current_tool_call = {
                                            "id": str(tool_call['id']),
                                            "type": "function",
                                            "function": {
                                                "name": tool_call.get('function', {}).get('name', ''),
                                                "arguments": tool_call.get('function', {}).get('arguments', '{}')
                                            }
                                        }
                                        if current_tool_call not in current_tool_calls:
                                            current_tool_calls.append(current_tool_call)
                                    elif current_tool_call and 'function' in tool_call:
                                        # Update existing tool call
                                        if 'name' in tool_call['function'] and tool_call['function']['name']:
                                            current_tool_call['function']['name'] = tool_call['function']['name']
                                        if 'arguments' in tool_call['function']:
                                            if not current_tool_call['function']['arguments'].strip('{}').strip():
                                                current_tool_call['function']['arguments'] = tool_call['function']['arguments']
                                            else:
                                                # Append to existing arguments, handling JSON chunks
                                                current_tool_call['function']['arguments'] = current_tool_call['function']['arguments'].rstrip('}') + tool_call['function']['arguments'].lstrip('{')
                                else:
                                    # Handle object format
                                    if hasattr(tool_call, 'id') and tool_call.id:
                                        # New tool call
                                        current_tool_call = {
                                            "id": str(tool_call.id),
                                            "type": "function",
                                            "function": {
                                                "name": getattr(tool_call.function, 'name', ''),
                                                "arguments": getattr(tool_call.function, 'arguments', '{}')
                                            }
                                        }
                                        if current_tool_call not in current_tool_calls:
                                            current_tool_calls.append(current_tool_call)
                                    elif current_tool_call and hasattr(tool_call, 'function'):
                                        # Update existing tool call
                                        if hasattr(tool_call.function, 'name') and tool_call.function.name:
                                            current_tool_call['function']['name'] = tool_call.function.name
                                        if hasattr(tool_call.function, 'arguments'):
                                            if not current_tool_call['function']['arguments'].strip('{}').strip():
                                                current_tool_call['function']['arguments'] = tool_call.function.arguments
                                            else:
                                                # Append to existing arguments, handling JSON chunks
                                                current_tool_call['function']['arguments'] = current_tool_call['function']['arguments'].rstrip('}') + tool_call.function.arguments.lstrip('{')

                                # Validate tool call is complete before proceeding
                                if current_tool_call:
                                    logger.debug(f"Current tool call state: {current_tool_call}")
                                    if not current_tool_call['id']:
                                        logger.warning("Tool call missing ID")
                                    if not current_tool_call['function']['name']:
                                        logger.warning("Tool call missing function name")

                            logger.debug(f"Current tool calls after processing: {current_tool_calls}")

                    # Create and add assistant message with complete content and tool calls
                    content = ''.join(current_content)
                    # Add usage metrics from the final chunk if available
                    if hasattr(chunk, 'usage'):
                        metrics["usage"] = {
                            "completion_tokens": getattr(chunk.usage, "completion_tokens", 0),
                            "prompt_tokens": getattr(chunk.usage, "prompt_tokens", 0),
                            "total_tokens": getattr(chunk.usage, "total_tokens", 0)
                        }
                    assistant_message = Message(
                        role="assistant",
                        content=content,
                        tool_calls=current_tool_calls if current_tool_calls else None,
                        metrics=metrics
                    )
                    thread.add_message(assistant_message)
                    yield StreamUpdate(StreamUpdate.Type.ASSISTANT_MESSAGE, assistant_message)

                    # If no tool calls, we're done
                    if not current_tool_calls:
                        break

                    # Execute tools and yield results
                    for tool_call in current_tool_calls:
                        try:
                            # Ensure we have valid JSON for arguments
                            args = tool_call['function']['arguments']
                            if not args.strip():
                                args = '{}'
                            # Parse arguments to ensure valid JSON
                            try:
                                parsed_args = json.loads(args)
                            except json.JSONDecodeError:
                                # If invalid JSON, try to fix common streaming artifacts
                                args = args.strip().rstrip(',').rstrip('"')
                                if not args.endswith('}'):
                                    args += '}'
                                if not args.startswith('{'):
                                    args = '{' + args
                                parsed_args = json.loads(args)

                            tool_call['function']['arguments'] = json.dumps(parsed_args)
                            
                            # Track tool execution time
                            tool_start_time = datetime.now(UTC)
                            result = await self._handle_tool_execution(tool_call)
                            
                            # Create tool metrics including weave_call info if available
                            tool_metrics = {
                                "model": self.model_name,
                                "timing": {
                                    "started_at": tool_start_time.isoformat(),
                                    "ended_at": datetime.now(UTC).isoformat(),
                                    "latency": (datetime.now(UTC) - tool_start_time).total_seconds() * 1000
                                }
                            }
                            if "weave_call" in metrics:
                                tool_metrics["weave_call"] = metrics["weave_call"]
                            
                            tool_message = Message(
                                role="tool",
                                content=result["content"],
                                name=result.get("name", tool_call["function"]["name"]),
                                tool_call_id=tool_call["id"],
                                metrics=tool_metrics
                            )
                            thread.add_message(tool_message)
                            yield StreamUpdate(StreamUpdate.Type.TOOL_MESSAGE, tool_message)
                        except Exception as e:
                            yield StreamUpdate(StreamUpdate.Type.ERROR, f"Tool execution failed: {str(e)}")
                            # Continue with next tool rather than breaking completely

                    # Reset for next iteration
                    current_content = []
                    current_tool_calls = []
                    current_tool_call = None
                    api_start_time = None
                    self._iteration_count += 1

                except Exception as e:
                    yield StreamUpdate(StreamUpdate.Type.ERROR, f"Completion failed: {str(e)}")
                    break

            # Handle max iterations
            if self._iteration_count >= self.max_tool_iterations:
                message = Message(
                    role="assistant",
                    content="Maximum tool iteration count reached. Stopping further tool calls.",
                    metrics={
                        "model": self.model_name,
                        "timing": {
                            "started_at": datetime.now(UTC).isoformat(),
                            "ended_at": datetime.now(UTC).isoformat(),
                            "latency": 0
                        }
                    }
                )
                thread.add_message(message)
                yield StreamUpdate(StreamUpdate.Type.ASSISTANT_MESSAGE, message)

            # Save final state if using thread store
            if self.thread_store:
                await self.thread_store.save(thread)

            # Yield final complete update
            new_messages = [m for m in thread.messages if m.role != "user"]
            yield StreamUpdate(StreamUpdate.Type.COMPLETE, (thread, new_messages))

        except Exception as e:
            yield StreamUpdate(StreamUpdate.Type.ERROR, f"Stream processing failed: {str(e)}")
            raise  # Re-raise to ensure error is properly propagated

        finally:
            # Reset iteration count
            self._iteration_count = 0 