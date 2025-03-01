"""
Translation Service Client Operations

This module provides functionality for:
- Preparing files for translation (converting between formats if needed)
- Uploading files to translation service
- Monitoring translation progress
- Downloading completed translations
- Post-processing translated files

Typical flow:
    prepare_files → upload_file → start_translation → wait_for_translation → process_translated_file
"""

import asyncio
import json
import aiohttp
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from ..configs import ServerConfig, RetryConfig
from ..utils.convert_to_srt import convert_to_srt
from ..utils.srt_to_ass import srt_to_ass_using_template
from ..utils.fix_rtl import fix_rtl

# =========================================================
# Data models
# =========================================================

@dataclass(frozen=True)
class UploadResponse:
    """Response received after successful file upload"""
    file_id: str
    price: int


@dataclass
class TranslationContext:
    """Contains all state related to a translation job"""
    original_path: Path           # Original input file path
    upload_path: Path             # Path of file actually uploaded (may be converted)
    is_ass_input: bool            # Whether input is ASS format needing conversion
    temp_srt_path: Path = None    # Temporary SRT path if converted from ASS
    file_id: str = None           # Server-assigned file ID after upload
    price: int = None             # Translation price
    downloaded_path: Path = None  # Path where translated file is saved
    output_path: Path = None      # Final output path after processing

# =========================================================
# File preparation and processing
# =========================================================

def prepare_files(file_path: str) -> TranslationContext:
    """
    Prepare files for translation, converting ASS to SRT if needed.
    
    Args:
        file_path: Path to the input subtitle file
        
    Returns:
        TranslationContext with prepared files
        
    Raises:
        RuntimeError: If file conversion fails
    """
    original_path = Path(file_path)
    is_ass_input = original_path.suffix.lower() == '.ass'
    temp_srt_path = None
    upload_path = original_path

    # Convert ASS to SRT if needed
    if is_ass_input:
        temp_srt_path = original_path.with_suffix('.srt')
        try:
            converted_path = convert_to_srt(str(original_path), str(temp_srt_path))
            if not converted_path:
                raise RuntimeError("ASS to SRT conversion failed")
            upload_path = temp_srt_path
        except Exception as e:
            if temp_srt_path:
                temp_srt_path.unlink(missing_ok=True)  # Cleanup temp file
            raise RuntimeError(f"Error converting input file: {str(e)}")

    return TranslationContext(
        original_path=original_path,
        upload_path=upload_path,
        is_ass_input=is_ass_input,
        temp_srt_path=temp_srt_path
    )


def process_translated_file(ctx: TranslationContext, prefix: str) -> None:
    """
    Process the translated file - convert SRT to ASS if needed and apply RTL fixing.
    
    Args:
        ctx: Translation context containing file paths
        prefix: Prefix to add to output filename
    """
    if ctx.is_ass_input:
        output_ass = ctx.original_path.with_name(f"{prefix}{ctx.original_path.name}")
        success = srt_to_ass_using_template(
            str(ctx.downloaded_path),
            str(ctx.original_path),
            str(output_ass)
        )
        if success:
            # Cleanup temporary files
            ctx.downloaded_path.unlink(missing_ok=True)
            if ctx.temp_srt_path:
                ctx.temp_srt_path.unlink(missing_ok=True)
            print(f"Final ASS file created: {output_ass}")
            # Apply RTL fixing to the ASS output
            fix_rtl(str(output_ass))
            print("RTL text formatting applied to ASS file")
            ctx.output_path = output_ass
    else:
        # Apply RTL fixing to SRT output
        fix_rtl(str(ctx.downloaded_path))
        print("RTL text formatting applied to SRT file")
        ctx.output_path = ctx.downloaded_path

# =========================================================
# API communication functions
# =========================================================

async def upload_file(session: aiohttp.ClientSession, file_path: Path, token: str, server_config: ServerConfig) -> UploadResponse:
    """
    Upload a file to the translation service.
    
    Args:
        session: HTTP client session
        file_path: Path to file for upload
        token: Authentication token
        server_config: Server configuration
        
    Returns:
        UploadResponse with file_id and price
        
    Raises:
        RuntimeError: If upload fails
    """
    headers = {"Token": token}
    
    # Create form data with the complete file information
    form = aiohttp.FormData()
    form.add_field('file',  # Use 'file' as field name as expected by server
                  file_path.read_bytes(),
                  filename=file_path.name,
                  content_type='text/plain')
    
    async with session.post(
        f"{server_config.api_base}{server_config.upload_path}",
        headers=headers,
        data=form
    ) as response:
        if response.status != 200:
            raise RuntimeError(f"Upload failed: {await response.text()}")
            
        data = await response.json()
        return UploadResponse(file_id=data["file_id"], price=data["price"])


async def start_translation(session: aiohttp.ClientSession, file_id: str, token: str, server_config: ServerConfig) -> None:
    """
    Initiate the translation process for an uploaded file.
    
    Args:
        session: HTTP client session
        file_id: ID of uploaded file
        token: Authentication token
        server_config: Server configuration
        
    Raises:
        RuntimeError: If translation start fails
    """
    headers = {"Token": token}
    
    async with session.get(
        f"{server_config.api_base}{server_config.translate_path.format(file_id=file_id)}",
        headers=headers
    ) as response:
        if response.status != 202:
            raise RuntimeError(f"Translation start failed: {await response.text()}")


async def download_file(session: aiohttp.ClientSession, file_id: str, token: str, 
                        original_path: Path, prefix: str, server_config: ServerConfig) -> Path | bool:
    """
    Download the translated file.
    
    Args:
        session: HTTP client session
        file_id: ID of file to download
        token: Authentication token
        original_path: Original file path (for naming)
        prefix: Prefix to add to the filename
        server_config: Server configuration
        
    Returns:
        Path to downloaded file if successful, False if file not ready
        
    Raises:
        RuntimeError: If download fails for reasons other than file not ready
    """
    headers = {"Token": token}
    
    try:
        async with session.get(
            f"{server_config.api_base}{server_config.download_path.format(file_id=file_id)}",
            headers=headers
        ) as response:
            if response.status == 200:
                # Save translation with prefix in same directory
                save_path = original_path.with_name(f"{prefix}{original_path.name}")
                save_path.write_bytes(await response.read())
                print(f"File downloaded successfully: {save_path.name}")
                return save_path
                
            if response.status in (404, 400):  # File not ready
                return False
                
            raise RuntimeError(f"Download failed: {await response.text()}")
            
    except aiohttp.ClientError as e:
        raise RuntimeError(f"Connection error: {str(e)}")

# =========================================================
# Status monitoring functions
# =========================================================

async def handle_websocket_messages(token: str, file_id: str, server_config: ServerConfig) -> bool:
    """
    Listen for WebSocket updates on translation progress.
    
    Args:
        token: Authentication token
        file_id: ID of file being translated
        server_config: Server configuration
        
    Returns:
        True if translation completed, False otherwise
    """
    import websockets
    
    try:
        async with websockets.connect(f"{server_config.ws_base}{server_config.ws_path}?token={token}") as ws:
            print("Connected to translation service. Waiting for updates...")
            
            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), 
                                    timeout=server_config.websocket_timeout)
                    data = json.loads(message)
                    
                    match data.get("event_type"):
                        case "status_update":
                            print(f"Status update: {data['data']}")
                            # Check if our file is translated
                            for file_info in data['data']:
                                if file_info['file_id'] == file_id:
                                    if file_info['translation_status'] == 'Translated':
                                        return True
                        case "complete":
                            print("All translations completed")
                            return True
                        case "error":
                            raise RuntimeError(f"Server error: {data['data']}")
                            
                except asyncio.TimeoutError:
                    print(f"[{datetime.now().isoformat()}] Connection timeout, sending ping...")
                    await ws.ping()
                    await asyncio.sleep(5)
                    
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed normally")
        return False
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e.code} - {e.reason}")
        return False

# =========================================================
# Retry and wait functions
# =========================================================

async def retry_download(
    session: aiohttp.ClientSession,
    file_id: str,
    token: str,
    original_path: Path,
    prefix: str,
    server_config: ServerConfig,
    max_retries: int = 10,
    retry_delay: int = 2
) -> Path | None:
    """
    Repeatedly try to download the translated file until success or max retries reached.
    
    Args:
        session: HTTP client session
        file_id: ID of file to download
        token: Authentication token
        original_path: Original file path (for naming)
        prefix: Prefix to add to the filename
        server_config: Server configuration
        max_retries: Maximum number of download attempts
        retry_delay: Seconds to wait between retries
        
    Returns:
        Path to downloaded file if successful, None if all retries failed
    """
    for retry in range(max_retries):
        try:
            downloaded_path = await download_file(
                session=session,
                file_id=file_id,
                token=token,
                original_path=original_path,
                prefix=prefix,
                server_config=server_config
            )
            if downloaded_path is not False:
                print(f"Download successful after retry {retry+1}")
                return downloaded_path
                
            print(f"Retry {retry+1}: Translation file not ready - waiting...")
            await asyncio.sleep(retry_delay)  # Wait between retries
        except Exception as e:
            print(f"Retry {retry+1} download error: {str(e)}")
            await asyncio.sleep(retry_delay)  # Wait between retries
    
    print("ERROR: Translation was completed on server but download failed after multiple attempts.")
    return None


async def wait_for_translation(session: aiohttp.ClientSession, ctx: TranslationContext, token: str, 
                               server_config: ServerConfig, retry_config: RetryConfig, prefix: str) -> bool:
    """
    Wait for translation to complete using both WebSocket and polling methods.
    
    Args:
        session: HTTP client session
        ctx: Translation context
        token: Authentication token
        server_config: Server configuration
        retry_config: Retry configuration
        prefix: Prefix to add to output filename
        
    Returns:
        True if translation completed and file downloaded, False otherwise
    """
    retry_count = 0
    
    while True:
        # Phase 1: Try WebSocket monitoring
        try:
            websocket_success = await asyncio.wait_for(
                handle_websocket_messages(token, ctx.file_id, server_config),
                timeout=300  # 5 minutes total timeout
            )
            if websocket_success:
                return True
        except asyncio.TimeoutError:
            retry_count = retry_config.websocket_reconnect_attempts  # Force download attempt

        # Phase 2: Check download endpoint after max retry attempts
        retry_count += 1
        if retry_count >= retry_config.websocket_reconnect_attempts:
            try:
                downloaded_path = await download_file(
                    session=session,
                    file_id=ctx.file_id,
                    token=token,
                    original_path=ctx.upload_path,
                    prefix=prefix,
                    server_config=server_config
                )
                if downloaded_path is not False:
                    ctx.downloaded_path = downloaded_path
                    return True
                print("Translation not ready - retrying...")
                retry_count = 0  # Reset counter after failed attempt
            except Exception as e:
                print(f"Download error: {str(e)}")
                retry_count = 0