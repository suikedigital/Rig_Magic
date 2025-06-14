"use client"

import { useState, useEffect } from "react"
import Image from "next/image"

interface ThemeAwareSplashScreenProps {
  // Function that returns a promise for API calls
  apiCall?: () => Promise<any>
  // Initial loading message
  initialMessage?: string
  // Minimum display time in ms (even if API resolves faster)
  minDisplayTime?: number
  // Maximum display time in ms (will fade out even if API hasn't resolved)
  maxDisplayTime?: number
  // Callback when splash screen completes
  onComplete?: (data?: any, error?: Error) => void
  // Show debug info (like request details)
  showDebugInfo?: boolean
  // Theme detection method
  themeDetection?: "auto" | "class" | "attribute" | "custom"
  // Custom theme detector function
  customThemeDetector?: () => "light" | "dark"
}

export default function ThemeAwareSplashScreen({
  apiCall,
  initialMessage = "Loading...",
  minDisplayTime = 1500,
  maxDisplayTime = 10000,
  onComplete,
  showDebugInfo = false,
  themeDetection = "auto",
  customThemeDetector,
}: ThemeAwareSplashScreenProps) {
  const [visible, setVisible] = useState(true)
  const [message, setMessage] = useState(initialMessage)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [debugInfo, setDebugInfo] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [isDark, setIsDark] = useState(false)

  // Theme detection logic
  useEffect(() => {
    const detectTheme = () => {
      if (customThemeDetector) {
        return customThemeDetector() === "dark"
      }

      switch (themeDetection) {
        case "class":
          return document.documentElement.classList.contains("dark")
        case "attribute":
          return document.documentElement.getAttribute("data-theme") === "dark"
        case "custom":
          // You can implement custom logic here
          return false
        case "auto":
        default:
          // Check for next-themes first
          const themeFromStorage = localStorage.getItem("theme")
          if (themeFromStorage === "dark" || themeFromStorage === "light") {
            return themeFromStorage === "dark"
          }
          // Fall back to system preference
          return window.matchMedia("(prefers-color-scheme: dark)").matches
      }
    }

    setIsDark(detectTheme())

    // Listen for theme changes
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)")
    const handleChange = () => setIsDark(detectTheme())

    mediaQuery.addEventListener("change", handleChange)

    // Also listen for storage changes (for next-themes)
    window.addEventListener("storage", handleChange)

    // Listen for class changes on document element
    const observer = new MutationObserver(handleChange)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class", "data-theme"],
    })

    return () => {
      mediaQuery.removeEventListener("change", handleChange)
      window.removeEventListener("storage", handleChange)
      observer.disconnect()
    }
  }, [themeDetection, customThemeDetector])

  useEffect(() => {
    const startTime = Date.now()
    let apiData: any = null
    let apiError: Error | null = null
    let progressInterval: NodeJS.Timeout
    let maxTimeoutId: NodeJS.Timeout

    // Function to handle completion
    const completeLoading = () => {
      const currentTime = Date.now()
      const elapsedTime = currentTime - startTime

      if (elapsedTime < minDisplayTime) {
        setTimeout(() => {
          setVisible(false)
          if (onComplete) onComplete(apiData, apiError || undefined)
        }, minDisplayTime - elapsedTime)
      } else {
        setVisible(false)
        if (onComplete) onComplete(apiData, apiError || undefined)
      }

      clearInterval(progressInterval)
      clearTimeout(maxTimeoutId)
    }

    // Set up progress animation
    progressInterval = setInterval(() => {
      setProgress((prev) => {
        const increment = !isLoading ? 5 : 1
        const newProgress = Math.min(prev + increment, 100)
        return newProgress
      })
    }, 100)

    // Set maximum timeout
    maxTimeoutId = setTimeout(() => {
      if (isLoading) {
        setError("Request timed out")
        setIsLoading(false)
        setMessage("Request timed out. Please try again.")
        setTimeout(completeLoading, 2000)
      }
    }, maxDisplayTime)

    // If there's an API call, execute it
    if (apiCall) {
      ;(async () => {
        try {
          setDebugInfo("Sending request...")
          apiData = await apiCall()
          setDebugInfo("Request successful!")
          setMessage("Success! Loading complete.")
          setIsLoading(false)
          setTimeout(completeLoading, 1000)
        } catch (err) {
          apiError = err as Error
          setError(apiError.message)
          setDebugInfo(`Error: ${apiError.message}`)
          setMessage("An error occurred. Please try again.")
          setIsLoading(false)
          setTimeout(completeLoading, 2000)
        }
      })()
    } else {
      setTimeout(() => {
        setIsLoading(false)
        setMessage("Ready!")
        setTimeout(completeLoading, 500)
      }, minDisplayTime - 500)
    }

    return () => {
      clearInterval(progressInterval)
      clearTimeout(maxTimeoutId)
    }
  }, [apiCall, minDisplayTime, maxDisplayTime, onComplete, isLoading, initialMessage])

  const containerClasses = `fixed inset-0 flex items-center justify-center z-50 ${
    visible ? "animate-fade-in" : "animate-fade-out"
  } ${isDark ? "bg-gray-900" : "bg-white"}`

  const textColor = error ? "text-red-500" : isDark ? "text-blue-400" : "text-blue-600"

  const ringColor = error ? "#ef4444" : isDark ? "#60a5fa" : "#2563eb"

  return (
    <div className={containerClasses}>
      <div className="flex flex-col items-center justify-center">
        <div className="relative">
          {/* Circular loading indicator */}
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <svg className="absolute inset-0" width="288" height="288" viewBox="0 0 288 288">
              <circle
                cx="144"
                cy="144"
                r="140"
                fill="none"
                strokeWidth="4"
                stroke={ringColor}
                strokeLinecap="round"
                strokeDasharray="879.2"
                strokeDashoffset={879.2 - (879.2 * progress) / 100}
                transform="rotate(-90 144 144)"
                className="transition-all duration-300 ease-in-out"
              />
            </svg>
          </div>

          {/* Logo */}
          <div className="w-64 h-64 relative z-0">
            <Image src="/Logo.png" alt="Rig Magic" fill className="object-contain" priority />
          </div>
        </div>

        {/* Status message */}
        <div className="mt-8 text-center">
          <p className={`text-xl font-medium ${textColor}`}>{message}</p>

          {/* Debug info */}
          {showDebugInfo && debugInfo && (
            <p className={`text-sm mt-2 ${isDark ? "text-gray-400" : "text-gray-600"}`}>{debugInfo}</p>
          )}
        </div>
      </div>
    </div>
  )
}
