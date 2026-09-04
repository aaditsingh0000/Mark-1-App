package com.mark1.android

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

class MemoryStore(context: Context) {
    private val prefs = context.getSharedPreferences("aven_memory", Context.MODE_PRIVATE)
    private val key = "messages"

    fun add(role: String, text: String) {
        val messages = JSONArray(prefs.getString(key, "[]"))
        messages.put(JSONObject().put("role", role).put("text", text))
        while (messages.length() > 40) messages.remove(0)
        prefs.edit().putString(key, messages.toString()).apply()
    }

    fun history(): List<Pair<String, String>> {
        val messages = JSONArray(prefs.getString(key, "[]"))
        return buildList {
            for (i in 0 until messages.length()) {
                val item = messages.optJSONObject(i) ?: continue
                add(item.optString("role") to item.optString("text"))
            }
        }
    }

    fun clear() {
        prefs.edit().remove(key).apply()
    }
}
