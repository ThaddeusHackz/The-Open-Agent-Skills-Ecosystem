---
name: hytopia-debugging
description: Helps debug HYTOPIA SDK games. Use when users need performance monitoring, error handling, client debugging, or troubleshooting. Covers debug panels, ErrorHandler, browser dev tools, and server logging.
---

# HYTOPIA Debugging

This skill helps you debug HYTOPIA SDK games effectively.

**Documentation:** https://dev.hytopia.com/sdk-guides/debugging

## When to Use This Skill

Use this skill when the user:

- Wants to see performance metrics (FPS, memory, latency)
- Needs to debug client-side UI issues
- Asks about server-side logging and errors
- Wants to troubleshoot network issues
- Needs to track entity positions
- Asks about error handling best practices

## Client Performance Debug Panel

### Accessing Debug Info

The HYTOPIA client provides real-time performance metrics:

**Keyboard:** Press the tilde key (`` ` ``) - typically top-left of keyboard

**Mobile:** Tap with 5 fingers simultaneously anywhere on screen

**Persistent Debug:** Append `?debug` to your game URL for debug panel to persist across hot reloads

### Debug Panel Shows

- **FPS** - Frame rate (capped at device refresh rate due to vsync)
- **Memory usage** - Current memory consumption
- **Network latency** - Round trip time to server
- **Entity position** - Position of controlled entity

## Client & UI Debugging

### Browser Developer Tools

Access via:
- Menu: "View → Developer Tools"
- Right-click: Select "Inspect"

### Console Tab

```typescript
// All console.log() calls from UI code appear here
console.log('Player clicked button');
console.log('UI state:', uiState);

// Errors also appear with stack traces
console.error('Failed to load asset');
```

### Elements Tab

- View current DOM state
- Inspect UI element styles
- Debug layout issues
- Modify styles in real-time for testing

## Server-Side Debugging

### Terminal Output

Server logs appear in the terminal where you launched the HYTOPIA server:

```typescript
// Standard logging
console.log('Player joined:', player.username);
console.log('Game state:', gameState);

// Debug specific systems
console.log('[Physics] Collision detected:', entityA.id, entityB.id);
console.log('[AI] Enemy state changed:', enemy.state);
```

### ErrorHandler Class

The SDK provides native error logging with stack traces:

```typescript
import { ErrorHandler } from 'hytopia';

// Warning - non-critical issues
ErrorHandler.warn('Player inventory nearly full');

// Error - recoverable errors
ErrorHandler.error('Failed to load player data, using defaults');

// Fatal Error - unrecoverable, may crash
ErrorHandler.fatalError('Critical game state corruption detected');
```

### Error Handling Patterns

```typescript
// Wrap risky operations
function loadPlayerData(player: Player) {
  try {
    const data = loadFromStorage(player.id);
    return data;
  } catch (error) {
    ErrorHandler.error(`Failed to load data for ${player.username}: ${error}`);
    return getDefaultPlayerData();
  }
}

// Validate inputs
function handlePlayerAction(player: Player, action: string) {
  if (!action) {
    ErrorHandler.warn(`Empty action from ${player.username}`);
    return;
  }

  if (!isValidAction(action)) {
    ErrorHandler.error(`Invalid action "${action}" from ${player.username}`);
    return;
  }

  processAction(player, action);
}
```

## Debugging Patterns

### Debug Logging System

```typescript
const DEBUG = true;  // Set false in production

function debugLog(category: string, message: string, data?: any) {
  if (!DEBUG) return;

  const timestamp = new Date().toISOString();
  if (data) {
    console.log(`[${timestamp}] [${category}] ${message}`, data);
  } else {
    console.log(`[${timestamp}] [${category}] ${message}`);
  }
}

// Usage
debugLog('Physics', 'Raycast hit', { entity: entity.id, distance: 5.2 });
debugLog('Network', 'Player sync', { playerCount: world.players.length });
```

### Performance Monitoring

```typescript
function measurePerformance(name: string, fn: () => void) {
  const start = performance.now();
  fn();
  const duration = performance.now() - start;

  if (duration > 16) {  // More than one frame at 60fps
    console.warn(`[Performance] ${name} took ${duration.toFixed(2)}ms`);
  }
}

// Usage
measurePerformance('AI Update', () => {
  updateAllEnemies();
});
```

### Entity Debug Visualization

```typescript
// Log entity states for debugging
function debugEntity(entity: Entity) {
  console.log('Entity Debug:', {
    id: entity.id,
    position: entity.position,
    rotation: entity.rotation,
    velocity: entity.velocity,
    health: entity.getData('health'),
    state: entity.getData('state')
  });
}

// Periodic state dump
setInterval(() => {
  console.log('=== World State ===');
  console.log('Players:', world.players.length);
  console.log('Entities:', world.entities.length);
  world.players.forEach(p => {
    console.log(`  ${p.username}: ${JSON.stringify(p.position)}`);
  });
}, 10000);  // Every 10 seconds
```

### Network Debug

```typescript
// Track network events
world.onPlayerJoin = (player) => {
  console.log(`[Network] Player connected: ${player.username} (${player.id})`);
};

world.onPlayerLeave = (player) => {
  console.log(`[Network] Player disconnected: ${player.username}`);
};

// Log sync issues
function onSyncError(player: Player, error: string) {
  ErrorHandler.error(`[Sync] Player ${player.username}: ${error}`);
}
```

## Best Practices

1. **Use categories** - Prefix logs with system names ([Physics], [AI], [Network])
2. **Log levels** - Use console.log for info, console.warn for warnings, ErrorHandler for errors
3. **Include context** - Always include relevant IDs and state in logs
4. **Performance check** - Watch for operations taking more than 16ms
5. **Clean up for production** - Disable verbose logging in production builds
6. **Use ?debug URL** - Keeps debug panel visible during development

## Common Debugging Scenarios

### "Why isn't my entity moving?"

```typescript
// Check entity state
console.log('Entity position:', entity.position);
console.log('Entity velocity:', entity.velocity);
console.log('Has physics:', entity.hasComponent('physics'));
console.log('Is kinematic:', entity.isKinematic);
```

### "Why is FPS low?"

```typescript
// Profile expensive operations
console.time('AI Update');
updateAllEnemies();
console.timeEnd('AI Update');

console.time('Physics Tick');
world.physicsStep();
console.timeEnd('Physics Tick');
```

### "Why did player disconnect?"

```typescript
world.onPlayerLeave = (player) => {
  console.log('Player left:', {
    username: player.username,
    playTime: Date.now() - player.getData('joinTime'),
    lastPosition: player.position,
    lastAction: player.getData('lastAction')
  });
};
```
