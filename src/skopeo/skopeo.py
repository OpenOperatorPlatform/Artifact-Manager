import subprocess
import json
from typing import Optional

class SkopeoClient:
    """
    Skopeo client that sends requests to the Skopeo CLI to interact with container registries.
    """
    @staticmethod
    def image_exists(
        registry_url: str, image_name: str, image_tag: str, username: Optional[str] = None, password: Optional[str] = None
    ) -> bool:
        """
        Checks if a specific image tag exists in a container registry using Skopeo.

        :param registry_url: The base registry URL including the project (e.g., registry.example.com/project)
        :param image_name: The image name (e.g., nginx)
        :param image_tag: The image tag to check (e.g., latest)
        :param username: Optional username for authentication
        :param password: Optional password for authentication
        :return: True if the image exists, False if it does not.
        :raises RuntimeError: If authentication fails, repository does not exist, or connectivity issues occur.
        """
        full_repo_url = f"{registry_url.rstrip('/')}/{image_name}"
        skopeo_command = ["skopeo", "inspect", f"docker://{full_repo_url}:{image_tag}"]

        if username and password:
            skopeo_command.extend(["--creds", f"{username}:{password}"])

        try:
            subprocess.run(
                skopeo_command,
                check=True,
                capture_output=True,
                text=True
            )
            return True  # If the command succeeds, the image exists

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip().lower()  # Normalize error message

            # **Detect Invalid Credentials**
            if "invalid username/password" in error_message or "unauthorized" in error_message:
                raise RuntimeError("Authentication failed: Invalid username or password.")

            # **Detect Repository Not Found**
            if "project" in error_message and "not found" in error_message:
                raise RuntimeError(f"Image '{image_name}' not found in '{registry_url}'.")

            # **Detect Network Issues**
            if "no route to host" in error_message or "connection refused" in error_message:
                raise RuntimeError("Network error: Unable to reach the registry. Check connectivity.")

            return False  # If it's another error but not fatal, assume the image does not exist

        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse Skopeo output")
