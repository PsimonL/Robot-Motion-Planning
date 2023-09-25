# Set-ExecutionPolicy RemoteSigned

# Relative path
$directoryPath = ".\agent_output"
# Remove items
Remove-Item -Path $directoryPath\* -Force -Recurse

# .\empty-saved-weights.ps1