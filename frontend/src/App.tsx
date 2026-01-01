import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import { theme } from './theme';
import { useStore } from './store';
import { Sidebar } from './components/layout/Sidebar';
import { SlideNavigation } from './components/layout/SlideNavigation';
import { SlideContainer } from './components/layout/SlideContainer';
import { useUrlSync } from './hooks/useUrlSync';
import { colors, spacing } from './designTokens';

export default function App() {
  const { slideIndex, hasCalculated, isCalculating } = useStore();

  // Sync state with URL for iframe embedding
  useUrlSync();

  return (
    <MantineProvider theme={theme}>
      <div
        style={{
          display: 'flex',
          minHeight: '100vh',
          backgroundColor: colors.background.secondary,
        }}
      >
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <main
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            marginLeft: spacing.appShell.navbar.width,
            padding: spacing.lg,
          }}
        >
          {/* Slide Content */}
          <div
            style={{
              flex: 1,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <SlideContainer
              slideIndex={slideIndex}
              hasCalculated={hasCalculated}
              isCalculating={isCalculating}
            />
          </div>

          {/* Navigation */}
          <SlideNavigation />
        </main>
      </div>
    </MantineProvider>
  );
}
