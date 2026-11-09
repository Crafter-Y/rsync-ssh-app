# SPDX-License-Identifier: GPL-2.0-only
FROM ghcr.io/hassio-addons/base:21.0.9 AS rsync-build

# Keep the matching restricted wrapper and rsync patched together.
# Update the version and archive checksum together when upgrading rsync.
ARG RSYNC_VERSION=3.5.2
ARG RSYNC_SHA256=a10d591825251e070f74c98df3daad195def4ed81b4a2de16169026aea33f6c8
ADD --checksum=sha256:${RSYNC_SHA256} https://download.samba.org/pub/rsync/src/rsync-${RSYNC_VERSION}.tar.gz /tmp/rsync.tar.gz
# hadolint ignore=DL3018
RUN apk add --no-cache build-base pkgconf python3 acl-dev attr-dev libidn2-dev openssl-dev xxhash-dev zstd-dev lz4-dev popt-dev \
    && mkdir /src \
    && tar -xzf /tmp/rsync.tar.gz -C /src --strip-components=1
WORKDIR /src
RUN ./configure --prefix=/usr --disable-md2man \
    && make -j2 \
    && install -Dm755 rsync /out/usr/bin/rsync \
    && install -Dm755 support/rrsync /out/usr/bin/rrsync \
    && install -Dm644 COPYING /out/usr/share/licenses/rsync/COPYING \
    && install -Dm644 /tmp/rsync.tar.gz /out/usr/src/rsync.tar.gz

FROM ghcr.io/hassio-addons/base:21.0.9
# hadolint ignore=DL3018
RUN apk add --no-cache openssh-server openssh-keygen shadow python3 acl-libs attr libidn2 libcrypto3 libxxhash zstd-libs lz4-libs popt \
    && addgroup -g 1000 backup \
    && adduser -D -H -u 1000 -G backup -h /var/empty -s /bin/ash backup \
    && mkdir -p /var/empty /etc/ssh/authorized_keys /run/sshd \
    && chown root:root /var/empty \
    && chmod 0755 /var/empty

COPY --from=rsync-build /out/ /
COPY rootfs/ /
RUN chmod 0755 /usr/local/bin/backup-session /usr/local/bin/start-backup-service \
    /etc/s6-overlay/s6-rc.d/sshd/run /etc/s6-overlay/s6-rc.d/sshd/finish

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
ARG BUILD_REPOSITORY=Crafter-Y/rsync-ssh-app
LABEL io.hass.name="Rsync SSH" \
    io.hass.description="Restricted rsync backups over SSH" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.licenses="GPL-2.0-only" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
