"use client";

import { useEffect, useRef } from "react";
import {
  CandlestickSeries,
  ColorType,
  createChart,
  HistogramSeries,
  LineSeries,
  type Time,
} from "lightweight-charts";

export type MarketBar = {
  date: string;
  open?: string | number;
  high?: string | number;
  low?: string | number;
  close: string | number;
  volume?: number | null;
};

type MarketChartProps = {
  data: MarketBar[];
  mode?: "candles" | "line";
  currency?: string;
  height?: number;
};

export default function MarketChart({
  data,
  mode = "candles",
  currency = "INR",
  height = 420,
}: MarketChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const chart = createChart(container, {
      width: container.clientWidth,
      height,
      layout: {
        background: {
          type: ColorType.Solid,
          color: "#fafaf8",
        },
        textColor: "#777771",
        attributionLogo: true,
      },
      grid: {
        vertLines: { color: "rgba(23,23,23,0.045)" },
        horzLines: { color: "rgba(23,23,23,0.07)" },
      },
      rightPriceScale: {
        borderColor: "rgba(23,23,23,0.12)",
      },
      timeScale: {
        borderColor: "rgba(23,23,23,0.12)",
        timeVisible: false,
      },
      crosshair: { mode: 0 },
      localization: {
        priceFormatter: (price: number) =>
          new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency,
            maximumFractionDigits: 2,
          }).format(price),
      },
    });

    const normalized = data
      .filter((bar) => /^\d{4}-\d{2}-\d{2}$/.test(bar.date))
      .map((bar) => ({
        time: bar.date as Time,
        open: bar.open == null ? NaN : Number(bar.open),
        high: bar.high == null ? NaN : Number(bar.high),
        low: bar.low == null ? NaN : Number(bar.low),
        close: Number(bar.close),
        volume: bar.volume == null ? null : Number(bar.volume),
      }))
      .filter((bar) => Number.isFinite(bar.close) && bar.close > 0)
      .sort((a, b) => String(a.time).localeCompare(String(b.time)))
      .filter(
        (bar, index, bars) => index === 0 || bar.time !== bars[index - 1].time,
      );

    const validCandles = normalized.filter(
      (bar) =>
        [bar.open, bar.high, bar.low].every(
          (value) => Number.isFinite(value) && value > 0,
        ) &&
        bar.high >= Math.max(bar.open, bar.close, bar.low) &&
        bar.low <= Math.min(bar.open, bar.close, bar.high),
    );

    if (mode === "candles") {
      const candles = chart.addSeries(CandlestickSeries, {
        upColor: "#527b68",
        downColor: "#c45b51",
        borderUpColor: "#527b68",
        borderDownColor: "#c45b51",
        wickUpColor: "#527b68",
        wickDownColor: "#c45b51",
      });

      candles.setData(
        validCandles.map(({ time, open, high, low, close }) => ({
          time,
          open,
          high,
          low,
          close,
        })),
      );

      const volume = chart.addSeries(HistogramSeries, {
        priceScaleId: "volume",
        priceFormat: { type: "volume" },
        lastValueVisible: false,
        priceLineVisible: false,
      });

      volume.setData(
        validCandles
          .filter(
            (bar) =>
              bar.volume !== null &&
              Number.isFinite(bar.volume) &&
              bar.volume >= 0,
          )
          .map((bar) => ({
            time: bar.time,
            value: bar.volume as number,
            color:
              bar.close >= bar.open
                ? "rgba(82,123,104,0.35)"
                : "rgba(196,91,81,0.35)",
          })),
      );

      chart.priceScale("volume").applyOptions({
        scaleMargins: { top: 0.8, bottom: 0 },
        borderVisible: false,
      });
    } else {
      const line = chart.addSeries(LineSeries, {
        color: "#527b68",
        lineWidth: 2,
        priceLineVisible: false,
      });

      line.setData(
        normalized.map(({ time, close }) => ({
          time,
          value: close,
        })),
      );
    }

    chart.timeScale().fitContent();

    const resizeObserver = new ResizeObserver(() => {
      if (container.clientWidth > 0) {
        chart.applyOptions({
          width: container.clientWidth,
        });
      }
    });

    resizeObserver.observe(container);

    return () => {
      resizeObserver.disconnect();
      chart.remove();
    };
  }, [data, mode, currency, height]);

  const hasValidClose = data.some((bar) => {
    const close = Number(bar.close);
    return (
      /^\d{4}-\d{2}-\d{2}$/.test(bar.date) &&
      Number.isFinite(close) &&
      close > 0
    );
  });

  return (
    <div className="w-full overflow-hidden rounded-xl">
      <div ref={containerRef} className="w-full" />
      {!hasValidClose && (
        <p className="py-8 text-center text-sm text-black/40">
          No historical price data is available for this period.
        </p>
      )}
    </div>
  );
}
