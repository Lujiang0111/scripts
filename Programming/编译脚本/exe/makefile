PROJECT=example_lib_test

PROJECT_PATH=../../../../
DEPS_PATH=$(PROJECT_PATH)deps/
TARGET_PATH=$(PROJECT_PATH)bin/
TARGET_RELEASE_PATH=$(TARGET_PATH)release/
INCLUDE_PATH=$(PROJECT_PATH)include/
SERVER_PATH=server/
SERVER_LIB_PATH=$(SERVER_PATH)lib/
SERVER_PLUGIN_PATH=$(SERVER_PATH)plugin/

GLOBAL_PATH=../../../../../../../../../
VERSION_BASELIB_PATH=$(GLOBAL_PATH)Versions/Baselib/
VERSION_ENGINE_PATH=$(GLOBAL_PATH)Versions/Engine/
VERSION_FABRICS_PATH=$(GLOBAL_PATH)Versions/Fabrics/
VERSION_PLUGINS_PATH=$(GLOBAL_PATH)Versions/Plugins/

ifneq (,$(wildcard $(GLOBAL_PATH)compile.dep))
	include $(GLOBAL_PATH)compile.dep
else
	LINK_RELEASE_WL_ADD=,-z,relro,-z,now,-z,noexecstack
	COMPILE_RELEASE_ITEM=-fstack-protector-all -fPIC -g
endif

# depends libs
# index 0 is project name
# index 1 is minimum version
PREBUILD_BASELIBS="libevent 2.1.12 \
example_lib 1.0.0"
PREBUILD_ENGINE=""
PREBUILD_FABRICS=""

POSTBUILD_BASELIBS="libevent 2.1.12 \
example_lib 1.0.0"
POSTBUILD_ENGINE=""
POSTBUILD_FABRICS=""
POSTBUILD_PLUGINS=""

INCLUDE=-I$(INCLUDE_PATH) \
-I$(PROJECT_PATH)internal \
-I$(DEPS_PATH)include \
-I$(DEPS_PATH)include/example_lib

WARNINGS=-Wall -Wno-unused-function
LIBS=-L$(DEPS_PATH)lib -Wl,-rpath-link=$(DEPS_PATH)lib -lexample_lib -levent
DEFINES=

CC:=gcc
CXX:=g++
TARGET=$(TARGET_PATH)$(PROJECT)
TARGET_RELEASE=$(TARGET_RELEASE_PATH)$(PROJECT)
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
	rm -rf $(SERVER_PATH)
	mkdir -p $(SERVER_PATH)
	\cp -r $(TARGET_PATH)* $(SERVER_PATH)
	\cp -r *.sh $(SERVER_PATH)

	python3 postbuild.py debug $(SERVER_LIB_PATH) $(VERSION_BASELIB_PATH) $(POSTBUILD_BASELIBS)
	python3 postbuild.py debug $(SERVER_LIB_PATH) $(VERSION_ENGINE_PATH) $(POSTBUILD_ENGINE)
	python3 postbuild.py debug $(SERVER_LIB_PATH) $(VERSION_FABRICS_PATH) $(POSTBUILD_FABRICS)
	python3 postbuild.py debug $(SERVER_PLUGIN_PATH) $(VERSION_PLUGINS_PATH) $(POSTBUILD_PLUGINS)
	
postbuild_release: mainbuild_release
	rm -rf $(SERVER_PATH)
	mkdir -p $(SERVER_PATH)
	\cp -r $(TARGET_RELEASE_PATH)\* $(SERVER_PATH)
	\cp -r *.sh $(SERVER_PATH)

	python3 postbuild.py release $(SERVER_LIB_PATH) $(VERSION_BASELIB_PATH) $(POSTBUILD_BASELIBS)
	python3 postbuild.py release $(SERVER_LIB_PATH) $(VERSION_ENGINE_PATH) $(POSTBUILD_ENGINE)
	python3 postbuild.py release $(SERVER_LIB_PATH) $(VERSION_FABRICS_PATH) $(POSTBUILD_FABRICS)
	python3 postbuild.py release $(SERVER_PLUGIN_PATH) $(VERSION_PLUGINS_PATH) $(POSTBUILD_PLUGINS)

$(TARGET): $(COBJ) $(CPPOBJ) $(CCOBJ)
	$(CXX) $(WARNINGS) -g -o $(TARGET) $(COBJ) $(CPPOBJ) $(CCOBJ) $(LIBS)

$(TARGET_RELEASE): $(COBJ) $(CPPOBJ) $(CCOBJ)
	$(CXX) $(WARNINGS) -g -o $(TARGET_RELEASE) $(COBJ) $(CPPOBJ) $(CCOBJ) $(LIBS)
	strip -s $(TARGET_RELEASE)

%.o: %.c
	$(CC) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $<

%.o: %.cpp
	$(CXX) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $< -std=c++11

%.o: %.cc
	$(CXX) $(DEFINES) $(WARNINGS) $(COMPILE_RELEASE_ITEM) $(INCLUDE) -o $@ -c $< -std=c++11

clean:
	-rm -f $(COBJ) $(CPPOBJ) $(CCOBJ) $(TARGET) $(TARGET_RELEASE)
