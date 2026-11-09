// SPDX-License-Identifier: GPL-2.0-only
import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const version = process.argv[2];
if (!/^\d+\.\d+\.\d+$/.test(version ?? '')) throw new Error('Expected a stable SemVer version');
const repository = process.env.GITHUB_REPOSITORY;
if (!repository || !/^[\w.-]+\/[\w.-]+$/.test(repository)) throw new Error('Missing repository');
const [owner] = repository.toLowerCase().split('/');
const configPath = 'rsync_ssh/config.yaml';
const config = readFileSync(configPath, 'utf8');
writeFileSync(configPath, config.replace(/^version:.*$/m, `version: "${version}"`));

for (const [arch, platform] of [['amd64', 'linux/amd64'], ['aarch64', 'linux/arm64']]) {
  const image = `ghcr.io/${owner}/${arch}-rsync-ssh`;
  execFileSync('docker', ['buildx', 'build', '--platform', platform, '--push',
    '--tag', `${image}:${version}`, '--tag', `${image}:latest`,
    '--build-arg', `BUILD_ARCH=${arch}`, '--build-arg', `BUILD_VERSION=${version}`,
    '--build-arg', `BUILD_DATE=${new Date().toISOString()}`,
    '--build-arg', `BUILD_REF=${process.env.GITHUB_SHA}`,
    '--build-arg', `BUILD_REPOSITORY=${repository}`, 'rsync_ssh'], { stdio: 'inherit' });
}
