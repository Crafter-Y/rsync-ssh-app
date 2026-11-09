// SPDX-License-Identifier: GPL-2.0-only
import { appendFileSync } from 'node:fs';
import semanticRelease from 'semantic-release';

const result = await semanticRelease({ dryRun: true });
if (result) appendFileSync(process.env.GITHUB_OUTPUT, `version=${result.nextRelease.version}\n`);
