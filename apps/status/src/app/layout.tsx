import type { Metadata } from "next";
import React from "react";

import "./globals.css";


export const metadata: Metadata = {
  title: "EVEData Status",
  description: "Status page for EVEData services",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  )
}
