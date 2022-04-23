include(CheckIncludeFileCXX)

add_subdirectory ( inspectors )

include ( FindPkgConfig )
pkg_search_module ( SNORT3 REQUIRED snort>=3 )
find_path ( tp_appid_module_api.h
    HINTS ${SNORT3_INCLUDE_DIRS}
    PATH_SUFFIXES "network_inspectors/appid" )

