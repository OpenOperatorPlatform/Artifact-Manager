from src.skopeo.skopeo import SkopeoClient
import pytest

def test_successful_image_exist():
    response = SkopeoClient.image_exists("docker.io/library/", "nginx", "latest")                                    
    assert response is True

def test_successful_image_not_exist():
    response = SkopeoClient.image_exists("docker.io/library/", "nginx", "not-existing-tag")
    assert response is False