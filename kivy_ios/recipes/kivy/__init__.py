from kivy_ios.toolchain import CythonRecipe
from os.path import join
import logging
import shutil

logger = logging.getLogger(__name__)


class KivyRecipe(CythonRecipe):
    """
    post kivy 2.0.0rc1
    Includes these iOS specific fixes:
    - Statusbar / Fullscreen fix (PR #4589)
    - Extend usage of certifi on iOS (PR #4648)
    """
    version = "067064c23a275187e67f1c9d7de7cc06f384af4d"
    url = "https://github.com/kivy/kivy/archive/{version}.zip"
    library = "libkivy.a"
    depends = ["sdl2", "sdl2_image", "sdl2_mixer", "sdl2_ttf", "ios",
               "pyobjus", "python", "host_setuptools3"]
    python_depends = ["certifi"]
    pbx_frameworks = ["Accelerate", "CoreMedia", "CoreVideo"]
    pre_build_ext = True

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env["KIVY_SDL2_PATH"] = ":".join([
            join(self.ctx.dist_dir, "include", "common", "sdl2"),
            join(self.ctx.dist_dir, "include", "common", "sdl2_image"),
            join(self.ctx.dist_dir, "include", "common", "sdl2_ttf"),
            join(self.ctx.dist_dir, "include", "common", "sdl2_mixer")])
        return env

    def build_arch(self, arch):
        self._patch_setup()
        super().build_arch(arch)

    def _patch_setup(self):
        # patch setup to remove some functionnalities
        pyconfig = join(self.build_dir, "setup.py")

        def _remove_line(lines, pattern):
            for line in lines[:]:
                if pattern in line:
                    lines.remove(line)

        def _sub_pattern(lines, pattern_old, pattern_new):
            for i, line in enumerate(lines[:]):
                if pattern_old in line:
                    lines[i] = lines[i].replace(pattern_old, pattern_new)

        with open(pyconfig) as fd:
            lines = fd.readlines()
        _remove_line(lines, "flags['libraries'] = ['GLESv2']")
        _sub_pattern(lines, "OpenGLES", "MetalANGLE")
        # _remove_line(lines, "c_options['use_sdl'] = True")
        with open(pyconfig, "w") as fd:
            fd.writelines(lines)

    def reduce_python_package(self):
        dest_dir = join(self.ctx.site_packages_dir, "kivy")
        shutil.rmtree(join(dest_dir, "tools"))
        shutil.rmtree(join(dest_dir, "tests"))


recipe = KivyRecipe()
