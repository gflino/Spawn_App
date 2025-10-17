[buildozer]
# Nível de log (2 para debug detalhado)
log_level = 2

# Aceitar automaticamente as licenças do SDK Android
android.accept_sdk_license = True

# Evita avisos sobre execução como root (útil em containers e CI)
warn_on_root = 0

# Modo silencioso de atualização
builddir = .buildozer
bin_dir = bin

[app]
# Nome do app
title = SpawnMGR

# Nome do pacote
package.name = spawnmgr

# Domínio reverso
package.domain = org.lino.zbc

# Diretório do código-fonte
source.dir = .

# Extensões incluídas
source.include_exts = py,kv,png,jpg,jpeg,json

# Pastas a excluir do build
source.exclude_dirs = tests, venv, .venv, __pycache__, .git, bin

# Versão
version = 0.1.0

# Requisitos Python
# Mantemos apenas o essencial — Kivy e pandas
requirements = python3,kivy==2.3.0,pandas

# Orientação
orientation = portrait

# Ícone (opcional, mas ajuda a evitar erros)
icon.filename = icon.png

# Permissões Android (adicione aqui se o app precisar)
android.permissions = 

# Arquiteturas Android
android.archs = arm64-v8a

# API do Android
android.api = 31
android.minapi = 21

# Versão do NDK
android.ndk_version = 25b

# Opções de build
android.allow_backup = True
fullscreen = 0

# Nome do pacote de saída
package.filename = SpawnMGR-${version}

# Desativa depuração no release (importante se for gerar release depois)
android.release_artifact = True

# Inclui cache de compilação
use_cache = True

# Define uma pasta de cache mais previsível (útil em CI)
android.p4a_dir = .buildozer/android/platform/python-for-android

# Evita falhas por ausência de SDK
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk

# Evita falhas por ausência de NDK
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk

# Define o compilador (mais estável)
android.ndk_api = 21
