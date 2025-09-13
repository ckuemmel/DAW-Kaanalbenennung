param(
    [Parameter(Mandatory = $true)] [string]$File,
    [Nullable[int]]$Spalte = $null,
    [string]$Spaltenname = $null,
    [string]$Blatt = $null,
    [Nullable[int]]$BlattIndex = $null,
    [Nullable[int]]$HeaderRow = $null,
    [switch]$SkipHeader,
    [switch]$Enter,
    [double]$Delay = 0.1,
    [switch]$Check,
    [int]$Preview = 10,
    [ValidateSet('windows','mac')] [string]$AutoNext,
    [switch]$AutoRun,
    [double]$NextDelay = 0.05
)

# Build argument list safely to avoid PowerShell parsing issues
$argsList = @(".\protools_tracknamer.py", $File)

if ($Spaltenname) { $argsList += @("--spaltenname", $Spaltenname) }
if ($Spalte -ne $null) { $argsList += @("--spalte", $Spalte) }
if ($Blatt) { $argsList += @("--blatt", $Blatt) }
if ($BlattIndex -ne $null) { $argsList += @("--blatt-index", $BlattIndex) }
if ($HeaderRow -ne $null) { $argsList += @("--header-row", $HeaderRow) }
if ($SkipHeader) { $argsList += @("--skip-header") }
if ($Enter) { $argsList += @("--enter") }

$argsList += @("--delay", [string]$Delay)

if ($Check) {
    $argsList += @("--check", "--preview", [string]$Preview)
}

if ($AutoNext) { $argsList += @("--auto-next", $AutoNext) }
if ($AutoRun) { $argsList += @("--auto-run") }
if ($NextDelay -ne $null) { $argsList += @("--next-delay", [string]$NextDelay) }

Write-Host "Starte: python $($argsList -join ' ')" -ForegroundColor Cyan
& python @argsList
exit $LASTEXITCODE
