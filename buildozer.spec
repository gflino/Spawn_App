[buildozer]
# (int) Nível de log (2 para debug)
log_level = 2
# (bool) Aceitar a licença do SDK automaticamente
android.accept_sdk_license = True
# (int) Avisar se o buildozer for executado como root
warn_on_root = 0

[app]
# (str) Título da sua aplicação
title = SpawnMGR

# (str) Nome do pacote (sem espaços ou caracteres especiais)
package.name = spawnmgr

# (str) Domínio do pacote (formato reverso)
package.domain = org.lino.zbc

# (str) Pasta do código-fonte ('.' significa a pasta atual)
source.dir = .

# (list) Extensões de ficheiros a incluir
source.include_exts = py,png,jpg,jpeg,kv,json

# (list) Pastas a excluir do pacote
source.exclude_dirs = tests, bin, venv*, .venv*

# (str) Versão da aplicação
version = 0.1

# (list) Requisitos da aplicação (apenas bibliotecas Python)
requirements = python3,kivy,pandas

# (str) Orientação suportada
orientation = portrait

# (str) Ícone da aplicação (o caminho é relativo à source.dir)
icon.filename = icon.png

# (list) Permissões Android
android.permissions = 

# (str) A arquitetura Android para a qual compilar
android.archs = arm64-v8a

# (int) API Android a usar
android.api = 31

# (int) API mínima requerida
android.minapi = 21

# (str) Versão do NDK
android.ndk_version = 25b

# (bool) Suporte a backup automático
android.allow_backup = True

# (int) Ecrã inteiro (0 para não, 1 para sim)
fullscreen = 0

