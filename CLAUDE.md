# CLAUDE.md - Guidelines for Salt-AMT Calculator

## Environment & Commands

### Frontend (React + Vite + Mantine)
- Install: `cd frontend && npm install`
- Dev server: `cd frontend && npm run dev`
- Build: `cd frontend && npm run build`
- Tests: `cd frontend && npx vitest run`
- Lint: `cd frontend && npm run lint`

### API (Modal + Python)
- Deploy: `cd api && unset MODAL_TOKEN_ID MODAL_TOKEN_SECRET && modal deploy modal_app.py`
- API base: `https://policyengine--salt-amt-api-{endpoint}.modal.run`

### Deployment
- Frontend: Vercel (configured via `vercel.json` at repo root)
- API: Modal (workspace: `policyengine`)

## Project Architecture
- **frontend/**: React SPA with Vite, Mantine UI, Recharts, Zustand
  - `src/components/slides/`: Slide components for the walkthrough
  - `src/components/inputs/`: Household and policy config input panels
  - `src/components/layout/`: Navigation, container, footer
  - `src/hooks/`: Custom hooks (URL sync, nationwide impacts data)
  - `src/api/client.ts`: Modal API client
  - `src/store.ts`: Zustand state management
  - `public/data/`: Pre-computed nationwide impacts JSON files (2026-2035)
- **api/**: Modal serverless Python API using PolicyEngine-US
  - Endpoints: health, calculate_single, calculate_salt_axis, calculate_income_axis, calculate_two_axes

## Code Style
- TypeScript with strict mode
- Functional React components with hooks
- Mantine v8 for UI components
- Recharts for all charts (not Plotly)
- Design tokens in `frontend/src/designTokens.ts`
