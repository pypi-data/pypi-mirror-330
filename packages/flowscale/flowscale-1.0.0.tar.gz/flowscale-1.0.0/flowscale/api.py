import os
import requests
from typing import Dict, Any, Optional, Union, BinaryIO
import mimetypes
from pathlib import Path
from .types import (
    HealthCheckResponse,
    QueueResponse,
    ExecuteWorkflowResponse,
    GetOutputResponse,
    RunDetailResponse,
    RunListResponse,
    CancelRunResponse,
)

class FlowscaleAPI:
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize the Flowscale API client.
        
        Args:
            api_key: The API key for authentication
            base_url: The base URL for the API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-API-KEY': api_key
        }
        
    def check_health(self) -> HealthCheckResponse:
        """
        Checks the health status of all ComfyUI instances within the specified cluster.
        
        Returns:
            The health status response
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/comfy/health",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def get_queue(self) -> QueueResponse:
        """
        Retrieves the queue data for all ComfyUI instances in the cluster.
        
        Returns:
            The queue status response
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/comfy/queue",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def execute_workflow(
        self, 
        workflow_id: str, 
        data: Dict[str, Any], 
        group_id: Optional[str] = None
    ) -> ExecuteWorkflowResponse:
        """
        Executes a specified workflow by processing dynamic form data.
        
        Args:
            workflow_id: The ID of the workflow to execute
            data: Form data including text fields and file uploads
            group_id: Optional group ID
            
        Returns:
            The workflow execution response
        """
        try:
            files = {}
            form_data = {}
            
            # Process the data into files and form fields
            for key, value in data.items():
                if hasattr(value, "read") and callable(value.read):
                    # It's a file-like object
                    files[key] = value
                elif isinstance(value, (list, tuple)):
                    # Handle arrays (for multiple files)
                    for i, item in enumerate(value):
                        if hasattr(item, "read") and callable(item.read):
                            files[f"{key}_{i}"] = item
                        else:
                            form_data[f"{key}_{i}"] = item
                elif isinstance(value, str) and os.path.isfile(value):
                    # It's a file path
                    file_name = os.path.basename(value)
                    files[key] = (file_name, open(value, "rb"), 
                                  mimetypes.guess_type(value)[0] or 'application/octet-stream')
                else:
                    # It's a regular value
                    form_data[key] = value
            
            # Construct the URL with query parameters
            url = f"{self.base_url}/api/v1/runs?workflow_id={workflow_id}"
            if group_id:
                url += f"&group_id={group_id}"
            
            response = requests.post(
                url,
                headers=self.headers,
                data=form_data,
                files=files
            )
            response.raise_for_status()
            
            # Close any opened files
            for file_tuple in files.values():
                if isinstance(file_tuple, tuple) and hasattr(file_tuple[1], 'close'):
                    file_tuple[1].close()
                
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def get_output(self, filename: str) -> Optional[GetOutputResponse]:
        """
        Retrieves the output of a specific run by providing the filename.
        
        Args:
            filename: The filename of the output to retrieve
            
        Returns:
            The output response or None if no output is found
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/runs/output",
                headers=self.headers,
                params={"filename": filename}
            )
            
            if response.status_code == 204:
                return None
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 204:
                return None
            elif error.response.status_code == 408:
                raise Exception("Run Timeout")
            else:
                self._handle_error(error)
        except Exception as error:
            self._handle_error(error)
    
    def cancel_run(self, run_id: str) -> CancelRunResponse:
        """
        Cancels a specific run using its unique run ID.
        
        Args:
            run_id: The ID of the run to cancel
            
        Returns:
            The cancellation response
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/runs/{run_id}/cancel",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def get_run(self, run_id: str) -> RunDetailResponse:
        """
        Retrieves detailed information about a specific run using its unique run ID.
        
        Args:
            run_id: The ID of the run to retrieve
            
        Returns:
            The run details response
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/runs/{run_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def get_runs(self, group_id: Optional[str] = None) -> RunListResponse:
        """
        Retrieves a list of all runs associated with a specific group ID.
        If no group ID is provided, all runs will be returned.
        
        Args:
            group_id: The group ID to filter runs
            
        Returns:
            The list of runs response
        """
        try:
            params = {"group_id": group_id} if group_id else {}
            response = requests.get(
                f"{self.base_url}/api/v1/runs",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as error:
            self._handle_error(error)
    
    def _handle_error(self, error: Exception) -> None:
        """
        Error handling helper.
        
        Args:
            error: The exception to handle
        """
        if isinstance(error, requests.exceptions.HTTPError):
            response = error.response
            raise Exception(
                f"Error: {response.status_code} {response.reason} - {response.text}"
            )
        elif isinstance(error, requests.exceptions.RequestException):
            raise Exception(f"Request error: {str(error)}")
        else:
            print(error)
            raise Exception(f"Error: {str(error)}")