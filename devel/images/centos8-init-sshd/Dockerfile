FROM centos:latest
MAINTAINER "Dominik Lenoch" <dlenoch@redhat.com>

CMD ["/sbin/init"]
STOPSIGNAL SIGRTMIN+3

#mask systemd-machine-id-commit.service - partial fix for https://bugzilla.redhat.com/show_bug.cgi?id=1472439
RUN systemctl mask systemd-remount-fs.service dev-hugepages.mount sys-fs-fuse-connections.mount \
    systemd-logind.service getty.target console-getty.service systemd-udev-trigger.service \
    systemd-udevd.service systemd-random-seed.service systemd-machine-id-commit.service

RUN dnf -y install passwd openssh-server procps-ng && dnf clean all && systemctl enable sshd.service
RUN echo "SomeSecretPassword0987" | passwd --stdin root
COPY identity.pub /root/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/init"]