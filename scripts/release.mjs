// SPDX-License-Identifier: GPL-2.0-only
import { readFileSync, writeFileSync } from 'node:fs';

const version = process.argv[2];
if (!/^\d+\.\d+\.\d+$/.test(version ?? '')) throw new Error('Expected a stable SemVer version');
if (process.env.RELEASE_VERSION !== version) throw new Error('Release version differs from built images');
const configPath = 'rsync_ssh/config.yaml';
const config = readFileSync(configPath, 'utf8');
writeFileSync(configPath, config.replace(/^version:.*$/m, `version: "${version}"`));
