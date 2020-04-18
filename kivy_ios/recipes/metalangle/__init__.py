from kivy_ios.toolchain import Recipe, shprint
from os.path import join
import sh


class MetalAngleFramework(Recipe):
    version = "master"
    url = "https://github.com/kakashidinho/metalangle/archive/{version}.zip"
    frameworks = [dict(name="MetalANGLE", path="ios/xcode/build/Release-{arch.sdk}/MetalANGLE.framework")]

    def prebuild_arch(self, arch):
        if self.has_marker("thirdparty_downloaded"):
            return
        shprint(sh.sh, join(self.build_dir, "ios", "xcode", "fetchDependencies.sh"))
        self.set_marker("thirdparty_downloaded")

    def build_arch(self, arch):
        shprint(sh.xcodebuild, self.ctx.concurrent_xcodebuild,
                "ONLY_ACTIVE_ARCH=NO",
                "ARCHS={}".format(arch.arch),
                "-sdk", arch.sdk,
                "-project", "ios/xcode/OpenGLES.xcodeproj",
                "-target", "MetalANGLE",
                "-configuration", "Release")


recipe = MetalAngleFramework()
