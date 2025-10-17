[buildozer]
# Nível de log (1 = info, 2 = debug)
log_level = 2

# Diretório onde o Buildozer criará os arquivos temporários
build_dir = .buildozer

# Aceita automaticamente as licenças do Android SDK
android.accept_sdk_license = True

# Força recompilações limpas (útil no Colab)
warn_on_root = 0

# Local padrão para os builds no Colab
storage_dir = /content/.buildozer_cache


[app]
# (str) Título da aplicação
title = SpawnMGR

# (str) Nome interno do pacote (não use espaços ou acentos)
package.name = SpawnMGR

# (str) Domínio do pacote (formato reverso)
package.domain = org.lino.zbc

# (str) Diretório do código-fonte
source.dir = .

# (list) Extensões de arquivos a incluir
source.include_exts = py,png,jpg,jpeg,kv,json

# (list) Diretórios a excluir do pacote
source.exclude_dirs = tests, bin, venv*, .venv*, .git

# (str) Ícone (opcional, se não existir o build usa um padrão)
icon.filename = icon.png

# (str) Versão da aplicação
version = 0.1.0

# (list) Bibliotecas Python que o app precisa
requirements = python3,kivy,pandas

# (str) Arquitetura Android
android.archs = arm64-v8a

# (int) API Android para compilar (31 é seguro e moderno)
android.api = 31

# (int) API mínima suportada
android.minapi = 21

# (str) Versão do NDK
android.ndk_version = 25b

# (bool) Suporte a multiplataforma
android.allow_backup = True

# (str) Orientação da tela
orientation = portrait

# (list) Permissões (adicione conforme necessário)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (bool) Evita crash ao abrir teclado virtual
android.hardwareAccelerated = true

# (str) Tema de janela
fullscreen = 0

# (str) Nome do executável
title_wm = SpawnMGR

# (bool) Habilita compilação incremental (útil após o primeiro build)
android.release_incremental = True


[buildozer_android]
# Força o uso de Java 17
java_version = 17

# Ativa o cache de dependências no Colab
sdk_path = /content/.buildozer_cache/android-sdk
ndk_path = /content/.buildozer_cache/android-ndk


[buildozer_requirements]
# Mantém compatibilidade com Cython
cython_version = 0.29.36
