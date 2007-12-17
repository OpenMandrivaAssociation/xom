# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%bcond_with test
%define gcj_support 1
%bcond_with bootstrap
%define section free

Summary:        XML Pull Parser
Name:           xom
Version:        1.1
Release:        %mkrel 0.0.2
Epoch:          0
License:        LGPL
URL:            http://www.xom.nu/
Group:          Development/Java
Source0:        http://www.cafeconleche.org/XOM/xom-%{version}-src.tar.gz
Patch0:         xom-1.1-remove-jaxen.patch
Patch1:         xom-1.1-clean-dist.patch
Patch2:         xom-1.1-compile15.patch
Patch3:         xom-1.1-remove_sun_import.patch
Patch4:         xom-1.1-build.patch
Patch5:         xom-1.1-sinjdoc.patch
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  jaxen
BuildRequires:  junit
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  icu4j
BuildRequires:  xml-commons-jaxp-1.3-apis

%if %without bootstrap
BuildRequires:  tagsoup
BuildRequires:  saxon
BuildRequires:  jaxp_parser_impl
BuildRequires:  xml-commons-resolver12
BuildRequires:  servlet
%endif
Requires:  xalan-j2
Requires:  xerces-j2
Requires:  icu4j
Requires:  xml-commons-jaxp-1.3-apis
%if !%{gcj_support}
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
XOM is a new XML object model. It is an open source (LGPL), 
tree-based API for processing XML with Java that strives 
for correctness, simplicity, and performance, in that order. 
XOM is designed to be easy to learn and easy to use. It 
works very straight-forwardly, and has a very shallow 
learning curve. Assuming you're already familiar with XML, 
you should be able to get up and running with XOM very quickly.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%if %without bootstrap
%package demo
Summary:        Samples for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
%{summary}.
%endif

%prep
%setup -q -n XOM
# remove all binary libs
%{_bindir}/find . -name "*.jar" -o -name "*.class" | %{_bindir}/xargs -t %{__rm}
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .orig
%{__perl} -pi -e 's/\r$//g' *.html *.txt
%{__perl} -pi -e 's/compress="no"/compress="yes"/g' build.xml

%build
export CLASSPATH=$(build-classpath icu4j jaxen)
export OPT_JAR_LIST="ant/ant-junit"
pushd lib
ln -sf $(build-classpath junit) junit.jar
ln -sf $(build-classpath xerces-j2) xercesImpl.jar
ln -sf $(build-classpath xalan-j2) xalan.jar
ln -sf $(build-classpath icu4j) normalizer.jar
ln -sf $(build-classpath xml-commons-jaxp-1.3-apis) xmlParserAPIs.jar
popd
mkdir lib2
%if %without bootstrap
pushd lib2
ln -sf $(build-classpath tagsoup) tagsoup-1.0rc1.jar
ln -sf $(build-classpath saxon) saxon.jar
ln -sf $(build-classpath jaxp_parser_impl) gnujaxp.jar
ln -sf $(build-classpath xml-commons-resolver12) resolver.jar
DOM4J_PRESENT=$(build-classpath dom4j 2>/dev/null || :)
if [ -n "$DOM4J_PRESENT" ]; then
ln -sf $(build-classpath dom4j) dom4j-1.5.1.jar
fi
ln -sf $(build-classpath servlet) servlet.jar
popd
%endif

%if %with bootstrap
%{ant} jar javadoc
%else
%{ant} jar samples javadoc
%if %with test
%{ant} test
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


rm -rf doc/{build.txt,api,api_impl}

# docs
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
install -m 644 overview.html $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
install -m 644 *.txt $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%if %without bootstrap
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 644 build/xom-samples.jar $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 644 xom.graffle $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif

%{_bindir}/find $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -type f | %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_datadir}/doc/%{name}-%{version}/overview.html
%{_datadir}/doc/%{name}-%{version}/README.txt
%{_datadir}/doc/%{name}-%{version}/LICENSE.txt
%{_datadir}/doc/%{name}-%{version}/Todo.txt
%{_datadir}/doc/%{name}-%{version}/lgpl.txt
%if %without bootstrap
%{_datadir}/%{name}-%{version}/xom.graffle
%endif
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%if %without bootstrap
%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}/xom-samples.jar
%endif
