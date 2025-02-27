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
            error_message = e.stderr.strip().lower()

            if "invalid username/password" in error_message or "unauthorized" in error_message:
                raise RuntimeError("Authentication failed: Invalid username or password.")

            if "project" in error_message and "not found" in error_message:
                raise RuntimeError(f"Image '{image_name}' not found in '{registry_url}'.")

            if "no route to host" in error_message or "connection refused" in error_message:
                raise RuntimeError("Network error: Unable to reach the registry.")

            if "no such host" in error_message or "name or service not known" in error_message:
                raise RuntimeError(f"DNS resolution failed: Unable to resolve '{registry_url}'.")

            return False

        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse Skopeo output")

    @staticmethod
    def copy_image(
        src_registry: str,
        src_image_name: str,
        src_image_tag: str,
        dst_registry: str,
        dst_image_name: str,
        dst_image_tag: str,
        src_username: Optional[str] = None,
        src_password: Optional[str] = None,
        dst_username: Optional[str] = None,
        dst_password: Optional[str] = None
    ) -> bool:
        """
        Copies a container image from one registry to another using Skopeo.
        """
        src_url = f"docker://{src_registry.rstrip('/')}/{src_image_name}:{src_image_tag}"
        dst_url = f"docker://{dst_registry.rstrip('/')}/{dst_image_name}:{dst_image_tag}"

        skopeo_command = ["skopeo", "copy", src_url, dst_url]

        if src_username and src_password:
            skopeo_command.extend(["--src-creds", f"{src_username}:{src_password}"])

        if dst_username and dst_password:
            skopeo_command.extend(["--dest-creds", f"{dst_username}:{dst_password}"])

        try:
            subprocess.run(skopeo_command, check=True, capture_output=True, text=True)
            return True  # If the command succeeds, the image was copied

        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip().lower()

            if "invalid username/password" in error_message or "unauthorized" in error_message:
                raise RuntimeError("Authentication failed: Invalid username or password.")

            if "no such image" in error_message:
                raise RuntimeError(f"Source image '{src_image_name}:{src_image_tag}' not found in '{src_registry}'.")

            if "no route to host" in error_message or "connection refused" in error_message:
                raise RuntimeError("Network error: Unable to reach one of the registries.")

            if "no such host" in error_message or "name or service not known" in error_message:
                raise RuntimeError(f"DNS resolution failed: Unable to resolve '{src_registry}' or '{dst_registry}'.")

            raise RuntimeError(f"Image copy failed: {error_message}")
