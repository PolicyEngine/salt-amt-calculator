/**
 * Header component with branding and controls.
 */

import { Group, Button, Text, Burger, Loader } from '@mantine/core';
import { IconCalculator } from '@tabler/icons-react';
import { colors, spacing, typography } from '@/designTokens';

interface HeaderProps {
  onMenuClick: () => void;
  menuOpened: boolean;
  onCalculate: () => void;
  isCalculating: boolean;
}

export function Header({ onMenuClick, menuOpened, onCalculate, isCalculating }: HeaderProps) {
  return (
    <header
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '64px',
        backgroundColor: colors.background.primary,
        borderBottom: `1px solid ${colors.border.light}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `0 ${spacing.lg}`,
        zIndex: 100,
      }}
    >
      <Group gap="md">
        <Burger
          opened={menuOpened}
          onClick={onMenuClick}
          size="sm"
          color={colors.gray[700]}
          aria-label="Toggle settings"
        />
        <div>
          <Text
            style={{
              fontSize: typography.fontSize.xl,
              fontWeight: typography.fontWeight.bold,
              color: colors.primary[600],
              lineHeight: 1.2,
            }}
          >
            SALTernative
          </Text>
          <Text
            style={{
              fontSize: typography.fontSize.xs,
              color: colors.text.secondary,
              lineHeight: 1,
            }}
          >
            SALT & AMT Tax Calculator
          </Text>
        </div>
      </Group>

      <Group gap="md">
        <Button
          size="md"
          leftSection={isCalculating ? <Loader size={16} color="white" /> : <IconCalculator size={18} />}
          onClick={onCalculate}
          disabled={isCalculating}
          style={{
            backgroundColor: colors.primary[500],
          }}
        >
          {isCalculating ? 'Calculating...' : 'Calculate'}
        </Button>
      </Group>
    </header>
  );
}
