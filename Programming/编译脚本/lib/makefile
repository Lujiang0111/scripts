VERSION_X=1
VERSION_Y=0
VERSION_Z=0
PROJECT=example_lib

PROJECT_PATH=../../../../
DEPS_PATH=$(PROJECT_PATH)deps/
TARGET_PATH=$(PROJECT_PATH)bin/
TARGET_RELEASE_PATH=$(TARGET_PATH)release/
INCLUDE_PATH=$(PROJECT_PATH)include/

GLOBAL_PATH=../../../../../../../../
VERSION_BASELIB_PATH=$(GLOBAL_PATH)Versions/Baselib/
VERSION_ENGINE_PATH=$(GLOBAL_PATH)Versions/Engine/
VERSION_FABRICS_PATH=$(GLOBAL_PATH)Versions/Fabrics/
VERSION_PLUGINS_PATH=$(GLOBAL_PATH)Versions/Plugins/Plugins/

ifneq (,$(wildcard $(GLOBAL_PATH)compile.dep))
	include $(GLOBAL_PATH)compile.dep
else
	LINK_RELEASE_WL_ADD=,-z,relro,-z,now,-z,noexecstack
	COMPILE_RELEASE_ITEM=-fstack-protector-all -fPIC -g
endif

# depends libs
# index 0 is project name
# index 1 is minimum version
PREBUILD_BASELIBS="libevent 2.1.12"
PREBUILD_ENGINE=""
PREBUILD_FABRICS=""

INCLUDE=-I$(INCLUDE_PATH) \
-I$(PROJECT_PATH)internal \
-I$(DEPS_PATH)include \
-I$(DEPS_PATH)include/libevent

WARNINGS=-Wall -Wno-unused-function
LIBS=-L$(DEPS_PATH)lib -Wl,-rpath-link=$(DEPS_PATH)lib -levent
DEFINES=

CC:=gcc
CXX:=g++
VERSION=$(VERSION_X).$(VERSION_Y).$(VERSION_Z)
REAL_NAME=lib$(PROJECT).so.$(VERSION)
SONAME=lib$(PROJECT).so.$(VERSION_X)
TARGET=$(TARGET_PATH)$(REAL_NAME)
TARGET_RELEASE=$(TARGET_RELEASE_PATH)$(REAL_NAME)
SRC_DIRS=$(PROJECT_PATH)src
CSRC=$(shell find $(SRC_DIRS) -name "*.c")
COBJ:=$(CSRC:.c=.o)
CPPSRC=$(shell find $(SRC_DIRS) -name "*.cpp")
CPPOBJ:=$(CPPSRC:.cpp=.o)
CCSRC=$(shell find $(SRC_DIRS) -name "*.cc")
CCOBJ:=$(CCSRC:.cc=.o)

.PHONY: all clean

all: postbuild

release: postbuild_release

prebuild:
	rm -rf $(DEPS_PATH)
	rm -rf $(TARGET_PATH)
	mkdir -p $(TARGET_PATH)
	python3 prebuild.py debug $(DEPS_PATH) $(VERSION_BASELIB_PATH) $(PREBUILD_BASELIBS)
	python3 prebuild.py debug $(DEPS_PATH) $(VERSION_ENGINE_PATH) $(PREBUILD_ENGINE)
	python3 prebuild.py debug $(DEPS_PATH) $(VERSION_FABRICS_PATH) $(PREBUILD_FABRICS)

prebuild_release:
	rm -rf $(DEPS_PATH)
	rm -rf $(TARGET_RELEASE_PATH)
	mkdir -p $(TARGET_RELEASE_PATH)
	python3 prebuild.py release $(DEPS_PATH) $(VERSION_BASELIB_PATH) $(PREBUILD_BASELIBS)
	python3 prebuild.py release $(DEPS_PATH) $(VERSION_ENGINE_PATH) $(PREBUILD_ENGINE)
	python3 prebuild.py release $(DEPS_PATH) $(VERSION_FABRICS_PATH) $(PREBUILD_FABRICS)

mainbuild: prebuild
	@$(MAKE) --no-print-directory $(TARGET)

mainbuild_release: prebuild_release
	@$(MAKE) --no-print-directory $(TARGET_RELEASE)

postbuild: mainbuild
	python3 postbuild.py debug $(TARGET_PATH) $(INCLUDE_PATH) $(VERSION_BASELIB_PATH) $(PROJECT) $(VERSION)

postbuild_release: mainbuild_release
	python3 postbuild.py release $(TARGET_RELEASE_PATH) $(INCLUDE_PATH) $(VERSION_BASELIB_PATH) $(PROJECT) $(VERSION)

$(TARGET): $(COBJ) $(CPPOBJ) $(CCOBJ)
	$(CXX) -shared -Wl,-soname,$(SONAME) $(WARNINGS) -g -o $(TARGET) $(COBJ) $(CPPOBJ) $(CCOBJ) $(LIBS)

$(TARGET_RELEASE): $(COBJ) $(CPPOBJ) $(CCOBJ)
	$(CXX) -shared -Wl,-soname,$(SONAME)$(LINK_RELEASE_WL_ADD) $(WARNINGS) -g -o $(TARGET_RELEASE) $(COBJ) $(CPPOBJ) $(CCOBJ) $(LIBS)
	strip -s $(TARGET_RELEASE)

%.o: %.c
	$(CC) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $<

%.o: %.cpp
	$(CXX) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $< -std=c++11

%.o: %.cc
	$(CXX) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $< -std=c++11

clean:
	-rm -f $(COBJ) $(CPPOBJ) $(CCOBJ) $(TARGET) $(TARGET_RELEASE)
