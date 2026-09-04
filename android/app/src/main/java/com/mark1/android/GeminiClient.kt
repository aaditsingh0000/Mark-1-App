package com.mark1.android

import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class GeminiClient {
    fun generate(apiKey: String, prompt: String, userText: String): Result<String> {
        return try {
            val url = URL("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$apiKey")
            val connection = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = "POST"
                connectTimeout = 15000
                readTimeout = 60000
                doOutput = true
                setRequestProperty("Content-Type", "application/json")
            }

            val request = JSONObject()
                .put(
                    "systemInstruction",
                    JSONObject().put(
                        "parts",
                        JSONArray().put(JSONObject().put("text", prompt))
                    )
                )
                .put(
                    "contents",
                    JSONArray().put(
                        JSONObject()
                            .put("role", "user")
                            .put("parts", JSONArray().put(JSONObject().put("text", userText)))
                    )
                )

            connection.outputStream.use { it.write(request.toString().toByteArray(Charsets.UTF_8)) }
            val body = (if (connection.responseCode in 200..299) connection.inputStream else connection.errorStream)
                .bufferedReader().use { it.readText() }

            if (connection.responseCode !in 200..299) {
                return Result.failure(IllegalStateException("Gemini HTTP ${connection.responseCode}: $body"))
            }

            val root = JSONObject(body)
            val text = root
                .optJSONArray("candidates")
                ?.optJSONObject(0)
                ?.optJSONObject("content")
                ?.optJSONArray("parts")
                ?.optJSONObject(0)
                ?.optString("text")
                ?.takeIf { !it.isNullOrBlank() }

            if (text == null) Result.failure(IllegalStateException("No text returned by Gemini"))
            else Result.success(text)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
