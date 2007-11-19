Name:		sshutout
Version:	1.0.4
Release:	%mkrel 1
Summary:	Daemon to Stop SSH Dictionary Attacks
License:	GPL
Group:		System/Servers
URL:		http://www.techfinesse.com/sshutout/sshutout.html
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		sshutout-1.0.4-mdv_conf.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	openssh-server
Requires:	iptables
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
This is a Linux daemon, that periodically monitors log
files looking for multiple failed login attempts via the Secure Shell
daemon (sshd, or optionally, sshd2). The daemon is meant to mitigate
what are commonly known as "dictionary attacks," i.e. scripted brute
force attacks that use lists of user ID's and passwords to effect
unauthorized intrusions. Typically such attacks fill the system logs
with hundreds or even thousands of log entries for the failed login
attempts. Aside from the nuisance of wasted space, wasted bandwidth,
and reduced signal to noise ratio in the logs, the attacks can pose a
real danger to systems with weak ID and password combinations.

The sshutout daemon blunts such attacks by creating firewall rules to
block individual offenders from accessing the system. These rules are
created when an attack signature is detected, and after a configurable
expiry interval has elapsed, the rules are deleted.

While sshutout can help reduce the severity and impact of dictionary
attacks, it is by no means a substitute for a good password policy. A
password policy is the front line of defense against intrusion and
should be given careful consideration. The sshutout daemon is merely
one small tool intended to help reduce log clutter and diminish the
incentive to mount dictionary attacks.

%prep
%setup -q
%patch0 -p1

%build
%{make} COMPILE="%{optflags} -Wall"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}/var/log

install -m0755 %{name} %{buildroot}%{_sbindir}/
install -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/
install -m0644 %{name}.8 %{buildroot}%{_mandir}/man8/

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# create ghostfiles
touch %{buildroot}/var/log/%{name}.log

%post
%create_ghostfile /var/log/%{name}.log root root 0644
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc License README sshutout.html
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %ghost %config(noreplace) /var/log/%{name}.log
