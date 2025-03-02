# Tarragon

Tarragon is text analogue of [dill](https://pypi.org/project/dill/) library.

### Poetry memos

1. Create poetry project structure
    ```
    poetry new .
    ```
   After that you can change files location.
2. Build poetry project to "dist" folder
    ```
    poetry build
    ``` 
3. Adding credentials for <REPO_NAME> repository into "%APPDATA%\pypoetry" folder or keyring (depends on default settings)
    ```
    poetry config http-basic.<REPO_NAME> __token__ <TOKEN>
    ```
4. Publish poetry project to <REPO_NAME> repository. Optional "--build" parameter makes rebuild
    ```
    poetry publish --build --repository <REPO_NAME>
    ```
   Remove "--repository" parameter for using default "pypi" repository.
5. Remove credentials for <REPO_NAME>
    ```
    poetry config --unset http-basic.<REPO_NAME>
    ```
6. Install poetry dependencies
    ```
    poetry lock
    poetry install
    ```