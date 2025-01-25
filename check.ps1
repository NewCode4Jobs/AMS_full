# Dependency Check and Install Script

# Function to check if an app is installed
function Check-Installed {
    param($Name, $CheckCommand)
    try {
        $result = Invoke-Expression $CheckCommand 2>$null
        Write-Host "$Name is INSTALLED" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "$Name is NOT installed" -ForegroundColor Red
        return $false
    }
}

# Check VSCode
Check-Installed -Name "VSCode" -CheckCommand "code --version"

# Check WinSurf IDE (if applicable)
Check-Installed -Name "WinSurf IDE" -CheckCommand "winsurf --version"

# Check Python
$pythonInstalled = Check-Installed -Name "Python" -CheckCommand "python --version"

# Check Pip
$pipInstalled = Check-Installed -Name "Pip" -CheckCommand "pip --version"

# If Python is installed, check other Python packages
if ($pythonInstalled) {
    # Check Uvicorn
    $uvicornInstalled = Check-Installed -Name "Uvicorn" -CheckCommand "python -m uvicorn --version"

    # Check FastAPI
    $fastapiInstalled = Check-Installed -Name "FastAPI" -CheckCommand "python -c 'import fastapi; print(fastapi.__version__)'"

    # Check SQLAlchemy
    $sqlalchemyInstalled = Check-Installed -Name "SQLAlchemy" -CheckCommand "python -c 'import sqlalchemy; print(sqlalchemy.__version__)'"

    # Check Pydantic
    $pydanticInstalled = Check-Installed -Name "Pydantic" -CheckCommand "python -c 'import pydantic; print(pydantic.__version__)'"
}
else {
    Write-Host "Python not found. Please install Python first." -ForegroundColor Red
}