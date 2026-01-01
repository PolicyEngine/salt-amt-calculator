/**
 * Drawer component for household and policy inputs.
 */

import { useState } from 'react';
import { Drawer, Tabs, Box, Text } from '@mantine/core';
import { IconHome, IconSettings } from '@tabler/icons-react';
import { HouseholdInputs } from '@/components/inputs/HouseholdInputs';
import { PolicyConfigInputs } from '@/components/inputs/PolicyConfigInputs';
import { colors, spacing, typography } from '@/designTokens';

interface InputDrawerProps {
  opened: boolean;
  onClose: () => void;
}

export function InputDrawer({ opened, onClose }: InputDrawerProps) {
  const [activeTab, setActiveTab] = useState<string | null>('household');

  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      title={
        <Text
          style={{
            fontSize: typography.fontSize.lg,
            fontWeight: typography.fontWeight.semibold,
            color: colors.primary[700],
          }}
        >
          Settings
        </Text>
      }
      padding="md"
      size="sm"
      position="left"
      styles={{
        header: {
          borderBottom: `1px solid ${colors.border.light}`,
          marginBottom: 0,
        },
        body: {
          padding: 0,
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100% - 60px)',
        },
      }}
    >
      <Tabs
        value={activeTab}
        onChange={setActiveTab}
        style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}
      >
        <Tabs.List>
          <Tabs.Tab value="household" leftSection={<IconHome size={16} />}>
            Household
          </Tabs.Tab>
          <Tabs.Tab value="policy" leftSection={<IconSettings size={16} />}>
            Policy
          </Tabs.Tab>
        </Tabs.List>

        <Box style={{ flex: 1, overflow: 'auto', padding: spacing.md }}>
          <Tabs.Panel value="household">
            <HouseholdInputs />
          </Tabs.Panel>

          <Tabs.Panel value="policy">
            <PolicyConfigInputs />
          </Tabs.Panel>
        </Box>
      </Tabs>
    </Drawer>
  );
}
