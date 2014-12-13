#!/bin/bash

set -e

ROOTDIR=$(cd `dirname $0`/..; pwd)
TREEISH="$1"
HOST=$2
RELEASE="dev`date +%y%m%d%H%M%S`"

[ -z "$TREEISH" ] && TREEISH="HEAD"
[ -z "$HOST" ] && HOST="butler"

WORKDIR=`mktemp -d /tmp/build.XXXXXXX`

retrieve_version() {
  echo ": $FUNCNAME:"
  pushd $ROOTDIR
  VERSION=`sed -n "s/^.*version='\(.*\)'.*$/\1/p" setup.py`
  echo ": $FUNCNAME: VERSION=$VERSION"
  popd
}

archive_repository() {
  local output="$1"
  local treeish="$2"
  echo ": $FUNCNAME: $treeish -> $output"

  pushd $ROOTDIR
  git archive --format=zip -o $output $treeish
  popd
}

modify_archive() {
  local archive="$1"
  local version="$2"
  local release="$3"
  echo ": $FUNCNAME: $archive -> $version -> $release"

  echo ": $FUNCNAME: unpacking"
  local archivedir="`dirname $archive`/mechanicalcrowd-platform-$version"
  unzip $archive -d "$archivedir"
  echo ": $FUNCNAME: modifing debian: $archivedir"
  set -f
  sed "s|(.*-.*)|\($version-$release\)|g" $archivedir/debian/changelog > `dirname $archivedir`/changelog
  mv `dirname $archivedir`/changelog  $archivedir/debian/changelog
  cat $archivedir/debian/changelog
  set +f
  echo ": $FUNCNAME: make archive"
  pushd `dirname $archive`
  tar czvf "`dirname $archive`/mechanicalcrowd-platform_${version}.orig.tar.gz" ./mechanicalcrowd-platform-$version
  ARCHIVE="`dirname $archive`/mechanicalcrowd-platform_${version}.orig.tar.gz"
}

build_archive() {
  local archive="$1"
  local version="$2"
  local release="$3"
  local host="$4"

  local directory=`ssh $host -- mktemp -d /tmp/build.XXXXXX`
  echo ": $FUNCNAME: copying $archive to $host:/$directory"
  scp $archive $host:/$directory
  echo ": $FUNCNAME: building"
  ssh $host -- "export LC_ALL=C; cd $directory; tar xzvf $directory/`basename $archive`; cd mechanicalcrowd-platform-$version; debuild -uc -us;"
  mkdir -p $ROOTDIR/build
  scp $host:/$directory/*.deb $ROOTDIR/build
}


ARCHIVE=$WORKDIR/mcrowd.zip
retrieve_version
archive_repository $ARCHIVE $TREEISH
modify_archive $ARCHIVE $VERSION $RELEASE
build_archive $ARCHIVE $VERSION $RELEASE $HOST
