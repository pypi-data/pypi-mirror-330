Name:      tuxtrigger
Version:   0.9.0
Release:   0%{?dist}
Summary:   FIXME
License:   MIT
URL:       https://tuxsuite.org/
Source0:   %{pypi_source}


BuildRequires: git
BuildRequires: make
BuildRequires: python3-PyYAML
BuildRequires: python3-devel
BuildRequires: python3-flit
BuildRequires: python3-pip
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cov
BuildRequires: python3-pytest-mock
Requires: python3-yaml
Requires: python3-jinja2
Requires: python3-requests



BuildArch: noarch

Requires: python3 >= 3.6

%global debug_package %{nil}

%description
TuxTrigger allows to automatically track a set of git repositories and branches.
When a change occurs, TuxTrigger will build, test and track the results using Tuxsuite and SQUAD.

%prep
%setup -q

%build
export FLIT_NO_NETWORK=1
make run
#make man
#make bash_completion

%check
python3 -m pytest test/

%install
mkdir -p %{buildroot}/usr/share/%{name}/
cp -r run %{name} %{buildroot}/usr/share/%{name}/
mkdir -p %{buildroot}/usr/bin
ln -sf ../share/%{name}/run %{buildroot}/usr/bin/%{name}
#mkdir -p %{buildroot}%{_mandir}/man1
#install -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/
#mkdir -p %{buildroot}/usr/share/bash-completion/completions/
#install -m 644 bash_completion/%{name} %{buildroot}/usr/share/bash-completion/completions/

%files
/usr/share/%{name}
%{_bindir}/%{name}
#%{_mandir}/man1/%{name}.1*
#/usr/share/bash-completion/completions/%{name}

%doc README.md
%license LICENSE

%changelog

* Tue Aug 30 2022 Pawel Szymaszek <pawel.szymaszek@linaro.org> - 0.0.1
- Initial version of the package
