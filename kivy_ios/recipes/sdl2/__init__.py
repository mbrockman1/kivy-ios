from kivy_ios.toolchain import Recipe, shprint
import sh
from os.path import join


class LibSDL2Recipe(Recipe):
    # version = "2.0.9"
    # url = "https://www.libsdl.org/release/SDL2-{version}.tar.gz"
    version = "metalangle"
    url = "https://github.com/misl6/SDL-mirror/archive/{version}.zip"
    library = "Xcode-iOS/SDL/build/Release-{arch.sdk}/libSDL2.a"
    include_dir = "include"
    depends = ["metalangle"]
    pbx_frameworks = ["AudioToolbox", "QuartzCore", "CoreGraphics", "CoreMotion",
                      "GameController", "AVFoundation", "Metal", "UIKit", "MetalANGLE"]

    def prebuild_arch(self, arch):
        if self.has_marker("patched"):
            return
        # self.apply_patch("uikit-transparent.patch")

        def _sub_pattern(lines, pattern_old, pattern_new):
            for i, line in enumerate(lines[:]):
                if pattern_old in line:
                    lines[i] = lines[i].replace(pattern_old, pattern_new)
        sdl2pbxproj = join(self.build_dir, "Xcode-iOS", "SDL", "SDL.xcodeproj", "project.pbxproj")
        with open(sdl2pbxproj) as fd:
            lines = fd.readlines()
        _sub_pattern(lines, "--YOURFRAMEMETALANGLEWORKPATH--", join(self.ctx.dist_dir, 'frameworks'))
        with open(sdl2pbxproj, "w") as fd:
            fd.writelines(lines)
        self.set_marker("patched")

    def build_arch(self, arch):
        env = arch.get_env()
        shprint(sh.xcodebuild, self.ctx.concurrent_xcodebuild,
                "ONLY_ACTIVE_ARCH=NO",
                "ARCHS={}".format(arch.arch),
                "CC={}".format(env['CC']),
                "-sdk", arch.sdk,
                "-project", "Xcode-iOS/SDL/SDL.xcodeproj",
                "-target", "libSDL-iOS",
                "-configuration", "Release")


recipe = LibSDL2Recipe()
