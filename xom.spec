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

#bcond_with test
%define with_test 0
%define gcj_support 0
#bcond_without bootstrap
%define with_bootstrap 0
%define section free

Summary:        XML Pull Parser
Name:           xom
Version:        1.2.1
Release:        2
Epoch:          0
License:        LGPL
URL:            http://www.xom.nu/
Group:          Development/Java
Source0:        http://www.cafeconleche.org/XOM/xom-1.2.1-src.tar.gz
Source1:        xom-1.2.1.pom
Patch0:         xom-1.2.1-remove_jaxen.patch
Patch1:         xom-1.1-clean-dist.patch
Patch2:         xom-1.1-compile15.patch
Patch3:         xom-1.1-remove_sun_import.patch
Patch4:         xom-1.1-build.patch
Patch5:         xom-1.1-sinjdoc.patch
Patch6:         xom-1.0-betterdocclasspath.patch
Patch7:         xom-1.2.1-gjdocissues.patch
Patch8:         xom-1.2.1-javadoc-stack-size.patch
Patch9:         xom-1.2.1-crosslinks.patch
Patch10:        xom-1.2.1-betterdoc-stack-size.patch

BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  java-javadoc
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  jaxen >= 1.1.2-1.3
BuildRequires:  junit
BuildRequires:  junit-javadoc
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  icu4j
BuildRequires:  xml-commons-jaxp-1.3-apis

%if !%with_bootstrap
BuildRequires:  tagsoup
BuildRequires:  saxon
BuildRequires:  saxon-aelfred
BuildRequires:  jaxp_parser_impl
#BuildRequires:  xml-commons-resolver12
BuildRequires:  xml-commons-resolver
BuildRequires:  servletapi5
%endif
Requires:  xalan-j2
Requires:  xerces-j2
Requires:  icu4j
Requires:  jaxen >= 1.1.2-1.3
Requires:  xml-commons-jaxp-1.3-apis
%if !%{gcj_support}
BuildArch:      noarch
BuildRequires:  java-devel
BuildRequires:  java-gcj-compat-devel
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
XML Pull Parser.

%if !%with_bootstrap
%package demo
Summary:        Samples for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
XML Pull Parser.
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
%patch6 -p1
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0


%{__perl} -pi -e 's/\r$//g' *.html *.txt
%{__perl} -pi -e 's/compress="no"/compress="yes"/g' build.xml

%build
export CLASSPATH=$(build-classpath icu4j jaxen)
export OPT_JAR_LIST="ant/ant-junit"
pushd lib
ln -sf $(build-classpath junit) junit.jar
ln -sf $(build-classpath xerces-j2) xercesImpl.jar
ln -sf $(build-classpath xerces-j2) dtd-xercesImpl.jar
ln -sf $(build-classpath xalan-j2) xalan.jar
ln -sf $(build-classpath icu4j) normalizer.jar
ln -sf $(build-classpath xml-commons-jaxp-1.3-apis) xmlParserAPIs.jar
popd
mkdir lib2
%if !%with_bootstrap
pushd lib2
ln -sf $(build-classpath tagsoup) tagsoup-1.2.jar
ln -sf $(build-classpath saxon) saxon.jar
ln -sf $(build-classpath saxon-aelfred) saxon.jar
ln -sf $(build-classpath jaxp_parser_impl) gnujaxp.jar
#ln -sf $(build-classpath xml-commons-resolver12) resolver.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar
DOM4J_PRESENT=$(build-classpath dom4j 2>/dev/null || :)
if [ -n "$DOM4J_PRESENT" ]; then
ln -sf $(build-classpath dom4j) dom4j-1.5.1.jar
fi
ln -sf $(build-classpath servletapi5) servlet.jar
popd

%endif

%if %with_bootstrap
ant \
  -Dant.build.javac.source=1.4 \
  -Dant.build.javac.target=1.4 \
  -Dbuild.sysclasspath=first \
  -Dj2se.api=%{_javadocdir}/java \
  -Djunit.api=%{_javadocdir}/junit \
  jar javadoc

%else

ant \
  -Dant.build.javac.source=1.4 \
  -Dant.build.javac.target=1.4 \
  -Dbuild.sysclasspath=first \
  -Dj2se.api=%{_javadocdir}/java \
  -Djunit.api=%{_javadocdir}/junit \
  jar samples betterdoc

%if %with_test
ant \
  -Dant.build.javac.source=1.4 \
  -Dant.build.javac.target=1.4 \
  -Dbuild.sysclasspath=first \
  test
%endif
%endif

pushd build/apidocs
  for f in `find -name \*.css -o -name \*.html`; do
    sed -i 's/\r//g' $f
  done
popd

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

%if !%with_bootstrap
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 644 build/xom-samples.jar $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 644 xom.graffle $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif

%{_bindir}/find $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} -type f | %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version} JPP %{name}

%post
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%{_datadir}/doc/%{name}-%{version}/overview.html
%{_datadir}/doc/%{name}-%{version}/README.txt
%{_datadir}/doc/%{name}-%{version}/LICENSE.txt
%{_datadir}/doc/%{name}-%{version}/Todo.txt
%{_datadir}/doc/%{name}-%{version}/lgpl.txt
%if !%with_bootstrap
%{_datadir}/%{name}-%{version}/xom.graffle
%endif
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%if !%with_bootstrap
%files demo
%{_datadir}/%{name}-%{version}/xom-samples.jar
%endif


%changelog

* Fri Nov 11 2011 gil <gil> 0:1.2.1-1.mga2
+ Revision: 166422
- update to 1.2.1 , added m2 pom

* Sun Jan 16 2011 dmorgan <dmorgan> 0:1.2b1-0.0.5.mga1
+ Revision: 20261
- Fix find of javac and boot strap
- imported package xom


* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.2b1-0.0.5mdv2011.0
+ Revision: 608225
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.2b1-0.0.4mdv2010.1
+ Revision: 524458
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.2b1-0.0.3mdv2009.1
+ Revision: 350879
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.2b1-0.0.2mdv2009.0
+ Revision: 136618
- restore BuildRoot

* Thu Dec 20 2007 David Walluck <walluck@mandriva.org> 0:1.2b1-0.0.2mdv2008.1
+ Revision: 135399
- build with gcj for now
- 1.2b1

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sun Dec 09 2007 David Walluck <walluck@mandriva.org> 0:1.1-0.0.1mdv2008.1
+ Revision: 116657
- 1.1

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-4.3mdv2008.0
+ Revision: 87300
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-4.2mdv2008.0
+ Revision: 53223
- use xml-commons-jaxp-1.3-apis and xml-commons-resolver12 explicitely
  instead of the generic xml-commons-apis and xml-commons-resolver which
  are provided by multiple packages (see bug #31473)

* Mon Apr 23 2007 David Walluck <walluck@mandriva.org> 0:1.0-4.1mdv2008.0
+ Revision: 17156
- Import xom



* Mon Apr 23 2007 David Walluck <walluck@mandriva.org> 0:1.0-4.1mdv2008.0
- release

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-4jpp
- Add option to build core on bootstrap
- Add gcj_support option

* Tue Feb 28 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-3jpp
- Remove dependency on clover10 (non-free)

* Sun Feb 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-2jpp
- First JPP 1.7 release

* Wed Aug 17 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- First JPP release
