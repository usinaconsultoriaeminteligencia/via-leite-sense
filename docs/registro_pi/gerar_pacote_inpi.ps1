# Gera o pacote do codigo-fonte e o resumo hash (SHA-512) para o registro de programa de computador no INPI.
# Uso (PowerShell 5.1, na raiz do repositorio):
#   powershell -ExecutionPolicy Bypass -File docs\registro_pi\gerar_pacote_inpi.ps1 -Ref HEAD
#   powershell -ExecutionPolicy Bypass -File docs\registro_pi\gerar_pacote_inpi.ps1 -Ref v1.0-inpi -Destino "D:\INPI"
# O pacote NAO vai para o INPI: so o hash. Guarde o .zip + MANIFESTO em 2 lugares; sem eles o registro nao prova o conteudo.
param(
    [string]$Ref = "HEAD",
    [string]$Destino = (Join-Path $env:USERPROFILE "Documents\INPI_ViaLeiteSense")
)
$ErrorActionPreference = "Stop"

$raiz = (git rev-parse --show-toplevel).Trim()
Set-Location $raiz
$commit = (git rev-parse $Ref).Trim()
$curto = $commit.Substring(0, 7)
$dataCommit = (git show -s --format=%cs $commit).Trim()

# 1) Checagem de dados pessoais nos arquivos versionados desse commit (CPF formatado e pastas sensiveis)
# CPFs ficticios conhecidos (demo do frontend e testes) ficam de fora
$ficticios = @("987.654.321-00", "111.111.111-11", "222.222.222-22")
$suspeitos = git grep -o -E "[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}" $commit -- . 2>$null |
    Where-Object { $ficticios -notcontains ($_ -split ":")[-1] }
$pastas = git ls-tree -r --name-only $commit | Where-Object { $_ -match "^(dados_reais|dados_utilizador)/" -and $_ -notmatch "\.gitkeep$|README" }
if ($suspeitos -or $pastas) {
    Write-Host "ATENCAO: possiveis dados pessoais no commit $curto :" -ForegroundColor Yellow
    $suspeitos | ForEach-Object { Write-Host "  CPF? $_" }
    $pastas    | ForEach-Object { Write-Host "  pasta sensivel: $_" }
    $resp = Read-Host "Revise antes de registrar. Continuar mesmo assim? (s/N)"
    if ($resp -ne "s") { exit 1 }
}

# 2) Pacote
New-Item -ItemType Directory -Force -Path $Destino | Out-Null
$nome = "via-leite-sense_${dataCommit}_${curto}"
$zip = Join-Path $Destino "$nome.zip"
git archive --format=zip -o $zip $commit
if (-not (Test-Path $zip)) { throw "git archive falhou" }

# 3) Hash
$hash = (Get-FileHash $zip -Algorithm SHA512).Hash
$tam = (Get-Item $zip).Length
$arquivos = (git ls-tree -r --name-only $commit | Measure-Object).Count

# 4) Manifesto (prova do que foi registrado)
$manifesto = Join-Path $Destino "$nome.MANIFESTO.txt"
@"
VIA LEITE SENSE - pacote para registro de programa de computador (INPI / e-Software)
Gerado em      : $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Repositorio    : github.com/usinaconsultoriaeminteligencia/via-leite-sense
Referencia     : $Ref
Commit         : $commit
Data do commit : $dataCommit
Arquivo        : $nome.zip ($tam bytes, $arquivos arquivos versionados)
Algoritmo      : SHA-512
Resumo hash    : $hash
"@ | Out-File -FilePath $manifesto -Encoding utf8

Write-Host ""
Write-Host "Pacote   : $zip"
Write-Host "Manifesto: $manifesto"
Write-Host "SHA-512  : $hash" -ForegroundColor Cyan
Write-Host "Copie o hash SEM omitir caracteres no campo 'resumo digital hash' do e-Software."
