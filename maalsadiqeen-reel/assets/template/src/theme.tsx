import React, { createContext, useContext } from "react";
import type { Palette } from "./types";

export const W = 1080;
export const H = 1920;

/** Paper & olive — the maalsadiqeen look. Override any token via content.brand.palette */
export const DEFAULT_PALETTE: Palette = {
  bgCenter: "#FCF7F1",
  bgMid: "#F3EEE6",
  bgEdge: "#D8D3CC",
  ink: "#2A2219",
  inkSoft: "#5B534A",
  green: "#0B5E1E",
  olive: "#808E74",
  oliveSoft: "#A9B39F",
  gold: "#B9AA8C",
  goldSoft: "#D6CDBB",
  maroon: "#7A2424",
  chip: "#EAF2E6",
};

export const F = {
  /** display naskh (headings, hooks, lightly vocalised text) */
  naskh: "Amiri, 'Noto Naskh Arabic', serif",
  /** fully vocalised text ≥ 56px — tighter, clearer mark placement */
  noto: "'Noto Naskh Arabic', Amiri, serif",
  /** UI / explanatory text */
  sans: "Vazirmatn, 'Noto Sans Arabic', sans-serif",
};

const Ctx = createContext<Palette>(DEFAULT_PALETTE);

export const ThemeProvider: React.FC<{
  palette?: Partial<Palette>;
  children: React.ReactNode;
}> = ({ palette, children }) => (
  <Ctx.Provider value={{ ...DEFAULT_PALETTE, ...(palette ?? {}) }}>
    {children}
  </Ctx.Provider>
);

export const useTheme = () => useContext(Ctx);
