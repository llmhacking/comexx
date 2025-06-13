import shutil
import tempfile
from tree_sitter import Language
import os
import subprocess
import tree_sitter_c, tree_sitter_java, tree_sitter_c_sharp, tree_sitter_cpp

def get_language_map():
    # clone_directory = os.path.join(tempfile.gettempdir(), "comex")
    # shared_languages = os.path.join(clone_directory, "languages.so")

    # grammar_repos = [
    #     # ("https://github.com/tree-sitter/tree-sitter-java", "09d650def6cdf7f479f4b78f595e9ef5b58ce31e"),
    #     # ("https://github.com/tree-sitter/tree-sitter-c-sharp", "3ef3f7f99e16e528e6689eae44dff35150993307")
    #     ("https://github.com/tree-sitter/tree-sitter-java", "a7db5227ec40fcfe94489559d8c9bc7c8181e25a"),
    #     ("https://github.com/tree-sitter/tree-sitter-c-sharp", "b5eb5742f6a7e9438bee22ce8026d6b927be2cd7"),
    #     ("https://github.com/tree-sitter/tree-sitter-c", "7fa1be1b694b6e763686793d97da01f36a0e5c12"),
    #     ("https://github.com/tree-sitter/tree-sitter-cpp", "56455f4245baf4ea4e0881c5169de69d7edd5ae7"),
    # ]
    # vendor_languages = []

    # for url, commit in grammar_repos:
    #     grammar = url.rstrip("/").split("/")[-1]
    #     vendor_language = os.path.join(clone_directory, grammar)
    #     vendor_languages.append(vendor_language)
    #     if os.path.isfile(shared_languages) and not os.path.exists(vendor_language):
    #         os.remove(shared_languages)
    #     elif not os.path.isfile(shared_languages) and os.path.exists(vendor_language):
    #         shutil.rmtree(vendor_language)
    #     elif not os.path.isfile(shared_languages) and not os.path.exists(vendor_language):
    #         pass
    #     else:
    #         continue
    #     print(f"Intial Setup: First time running COMEX on {grammar}")
    #     os.makedirs(vendor_language, exist_ok=True)
    #     subprocess.check_call(["git", "init"], cwd=vendor_language, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    #     subprocess.check_call(["git", "remote", "add", "origin", url], cwd=vendor_language, stdout=subprocess.DEVNULL,
    #                           stderr=subprocess.STDOUT)
    #     subprocess.check_call(["git", "fetch", "--depth=1", "origin", commit], cwd=vendor_language,
    #                           stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    #     subprocess.check_call(["git", "checkout", commit], cwd=vendor_language, stdout=subprocess.DEVNULL,
    #                           stderr=subprocess.STDOUT)

    # build_id = ""
    # for vendor_language in vendor_languages:
    #     commit_hash = get_commit_hash(vendor_language)
    #     if commit_hash:
    #         build_id += commit_hash
    #     else:
    #         build_id += "ERROR"
    # build_id_file = os.path.join(clone_directory, "build_id")
    #
    # # check if the build_id is the same as the one stored in the file
    # # if not, rebuild the shared library
    # if os.path.exists(build_id_file):
    #     with open(build_id_file, "r") as f:
    #         stored_build_id = f.read()
    #     if build_id != stored_build_id:
    #         os.remove(shared_languages)
    # else:
    #     if os.path.exists(shared_languages):
    #         os.remove(shared_languages)

    # Language.build_library(
    #     # Store the library in the `build` directory
    #     shared_languages,
    #     vendor_languages,
    # )
    # PYTHON_LANGUAGE = Language("build/my-languages.so", "python")
    JAVA_LANGUAGE = Language(tree_sitter_java.language())
    C_SHARP_LANGUAGE = Language(tree_sitter_c_sharp.language())
    C_LANGUAGE = Language(tree_sitter_c.language())
    CPP_LANGUAGE = Language(tree_sitter_cpp.language())
    # RUBY_LANGUAGE = Language("build/my-languages.so", "ruby")
    # GO_LANGUAGE = Language("build/my-languages.so", "go")
    # PHP_LANGUAGE = Language("build/my-languages.so", "php")
    # JAVASCRIPT_LANGUAGE = Language("build/my-languages.so", "javascript")

    # with open(build_id_file, "w") as f:
    #     f.write(build_id)

    return {
        # "python": PYTHON_LANGUAGE,
        "java": JAVA_LANGUAGE,
        "cs": C_SHARP_LANGUAGE,
        "c": C_LANGUAGE,
        "cpp": CPP_LANGUAGE,
        # "ruby": RUBY_LANGUAGE,
        # "go": GO_LANGUAGE,
        # "php": PHP_LANGUAGE,
        # "javascript": JAVASCRIPT_LANGUAGE,
    }
