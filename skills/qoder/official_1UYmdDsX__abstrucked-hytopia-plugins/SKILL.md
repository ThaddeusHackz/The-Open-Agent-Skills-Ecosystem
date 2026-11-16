---
name: hytopia-plugins
description: Helps create and use plugins in HYTOPIA SDK games. Use when users need to add NPM packages, create reusable modules, or extend game functionality. Covers plugin requirements, installation, and best practices.
---

# HYTOPIA Plugins

This skill helps you create and use plugins in HYTOPIA SDK games.

**Documentation:** https://dev.hytopia.com/sdk-guides/plugins

## When to Use This Skill

Use this skill when the user:

- Wants to add third-party libraries to their game
- Needs to install NPM packages
- Asks about creating reusable plugins
- Wants to share code between games
- Needs to understand plugin restrictions
- Asks about package requirements

## Plugin Basics

In HYTOPIA, **a plugin and an NPM package are synonymous**. You can:
- Use existing NPM packages
- Create your own plugins as NPM packages
- Share plugins with the community

## Plugin Requirements

### 1. No External Network Requests

Plugins cannot make outbound network requests. The HYTOPIA runtime blocks external requests except to whitelisted internal services.

```typescript
// NOT ALLOWED - will be blocked
fetch('https://external-api.com/data');
axios.get('https://some-service.com');

// ALLOWED - internal HYTOPIA services
// (handled through SDK APIs)
```

### 2. Must Be Public on NPM

Plugins must be published publicly on NPM. HYTOPIA's deployment pipeline automatically installs packages from package.json.

```json
// package.json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "my-hytopia-plugin": "^1.0.0"
  }
}
```

### 3. Terms Compliance

HYTOPIA reserves the right to blacklist plugins that violate their Developer Terms of Use:
- Data harvesting
- Unauthorized web content serving
- Other prohibited implementations

## Installing Plugins

Install plugins like any NPM package:

```bash
# Using bun
bun add lodash

# Using npm
npm install lodash

# Using yarn
yarn add lodash
```

Then import and use:

```typescript
import _ from 'lodash';

const shuffledPlayers = _.shuffle(world.players);
const groupedByTeam = _.groupBy(world.players, p => p.getData('team'));
```

## Creating Plugins

### Basic Plugin Structure

```
my-hytopia-plugin/
├── package.json
├── src/
│   └── index.ts
├── dist/
│   └── index.js
└── README.md
```

### package.json

```json
{
  "name": "my-hytopia-plugin",
  "version": "1.0.0",
  "description": "A useful plugin for HYTOPIA games",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "keywords": ["hytopia", "plugin", "game"],
  "author": "Your Name",
  "license": "MIT",
  "peerDependencies": {
    "hytopia": "^1.0.0"
  }
}
```

### Example Plugin: Damage Numbers

```typescript
// src/index.ts
import { Entity, Player, World } from 'hytopia';

export interface DamageNumberOptions {
  duration?: number;
  color?: string;
  fontSize?: number;
}

export class DamageNumbers {
  private world: World;
  private options: DamageNumberOptions;

  constructor(world: World, options: DamageNumberOptions = {}) {
    this.world = world;
    this.options = {
      duration: 1000,
      color: '#ff0000',
      fontSize: 24,
      ...options
    };
  }

  show(player: Player, damage: number, position: { x: number, y: number, z: number }) {
    const id = `damage-${Date.now()}`;

    player.sendUI({
      type: 'text',
      id,
      text: `-${damage}`,
      worldPosition: position,
      style: {
        color: this.options.color,
        fontSize: this.options.fontSize,
        fontWeight: 'bold'
      }
    });

    setTimeout(() => {
      player.removeUI(id);
    }, this.options.duration);
  }

  showToAll(damage: number, position: { x: number, y: number, z: number }) {
    for (const player of this.world.players) {
      this.show(player, damage, position);
    }
  }
}

export default DamageNumbers;
```

### Using Your Plugin

```typescript
import DamageNumbers from 'my-hytopia-plugin';

const damageNumbers = new DamageNumbers(world, {
  duration: 1500,
  color: '#ffff00'
});

// When entity takes damage
entity.onDamage = (damage: number) => {
  damageNumbers.showToAll(damage, entity.position);
};
```

## Plugin Patterns

### Utility Plugin

```typescript
// hytopia-utils/src/index.ts
export function randomInRange(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

export function randomElement<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}
```

### Component Plugin

```typescript
// hytopia-health-system/src/index.ts
import { Entity, Player } from 'hytopia';

export class HealthComponent {
  private entity: Entity;
  private maxHealth: number;
  private currentHealth: number;

  onDeath?: () => void;
  onDamage?: (damage: number, remaining: number) => void;
  onHeal?: (amount: number, remaining: number) => void;

  constructor(entity: Entity, maxHealth: number = 100) {
    this.entity = entity;
    this.maxHealth = maxHealth;
    this.currentHealth = maxHealth;
  }

  takeDamage(amount: number): boolean {
    this.currentHealth = Math.max(0, this.currentHealth - amount);
    this.onDamage?.(amount, this.currentHealth);

    if (this.currentHealth <= 0) {
      this.onDeath?.();
      return true;  // Entity died
    }
    return false;
  }

  heal(amount: number) {
    this.currentHealth = Math.min(this.maxHealth, this.currentHealth + amount);
    this.onHeal?.(amount, this.currentHealth);
  }

  getHealth(): number {
    return this.currentHealth;
  }

  getMaxHealth(): number {
    return this.maxHealth;
  }

  getHealthPercent(): number {
    return this.currentHealth / this.maxHealth;
  }
}
```

### World Plugin

```typescript
// hytopia-spawn-system/src/index.ts
import { World, Player, Vector3 } from 'hytopia';

export class SpawnSystem {
  private world: World;
  private spawnPoints: Vector3[] = [];
  private usedSpawns: Set<number> = new Set();

  constructor(world: World) {
    this.world = world;
  }

  addSpawnPoint(position: Vector3) {
    this.spawnPoints.push(position);
  }

  getSpawnPoint(): Vector3 {
    // Find unused spawn
    for (let i = 0; i < this.spawnPoints.length; i++) {
      if (!this.usedSpawns.has(i)) {
        this.usedSpawns.add(i);
        return this.spawnPoints[i];
      }
    }

    // All used, pick random
    return this.spawnPoints[Math.floor(Math.random() * this.spawnPoints.length)];
  }

  releaseSpawnPoint(position: Vector3) {
    const index = this.spawnPoints.findIndex(
      p => p.x === position.x && p.y === position.y && p.z === position.z
    );
    if (index !== -1) {
      this.usedSpawns.delete(index);
    }
  }

  spawnPlayer(player: Player) {
    const spawn = this.getSpawnPoint();
    player.setPosition(spawn);
  }
}
```

## Best Practices

1. **No network calls** - Design plugins to work offline
2. **Peer dependencies** - Use peerDependencies for HYTOPIA SDK
3. **TypeScript** - Provide type definitions for better DX
4. **Documentation** - Include README with examples
5. **Semantic versioning** - Follow semver for updates
6. **Minimal dependencies** - Keep plugin lightweight
7. **Test locally** - Test before publishing to NPM

## Publishing Checklist

- [ ] No external network requests in code
- [ ] Published publicly on NPM
- [ ] Includes TypeScript types
- [ ] Has clear documentation
- [ ] Uses peerDependencies for hytopia
- [ ] Follows HYTOPIA Developer Terms
