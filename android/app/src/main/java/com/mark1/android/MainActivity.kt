package com.mark1.android

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import androidx.compose.material3.ExperimentalMaterial3Api

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { AvenApp() }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AvenApp() {
    val context = LocalContext.current
    val secureStore = remember { SecureKeyStore(context) }
    val memory = remember { MemoryStore(context) }
    val scope = rememberCoroutineScope()
    val gemini = remember { GeminiClient() }

    var apiKey by remember { mutableStateOf(secureStore.readApiKey().orEmpty()) }
    var draftKey by remember { mutableStateOf(apiKey) }
    var userText by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(memory.history()) }
    var busy by remember { mutableStateOf(false) }
    var status by remember { mutableStateOf("Ready") }
    var showSettings by remember { mutableStateOf(false) }

    val micLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        status = if (granted) "Microphone permission granted" else "Microphone permission denied"
    }

    MaterialTheme {
        Scaffold(topBar = {
            TopAppBar(
                title = { Text("Aven") },
                actions = { OutlinedButton(onClick = { showSettings = true }) { Text("API") } }
            )
        }) { padding ->
            Column(
                modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Text(status, style = MaterialTheme.typography.labelMedium)
                LazyColumn(modifier = Modifier.weight(1f).fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(messages) { (role, text) ->
                        Text(if (role == "user") "You: $text" else "Aven: $text")
                    }
                }
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = userText,
                        onValueChange = { userText = it },
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("Ask Aven…") },
                        maxLines = 4
                    )
                    Button(
                        enabled = !busy && userText.isNotBlank() && apiKey.isNotBlank(),
                        onClick = {
                            val text = userText.trim()
                            userText = ""
                            memory.add("user", text)
                            messages = memory.history()
                            busy = true
                            status = "Thinking…"
                            scope.launch(Dispatchers.IO) {
                                val prompt = context.assets.open("prompt.txt").bufferedReader().use { it.readText() }
                                val result = gemini.generate(apiKey, prompt, text)
                                launch(Dispatchers.Main) {
                                    busy = false
                                    result.onSuccess {
                                        memory.add("assistant", it)
                                        messages = memory.history()
                                        status = "Ready"
                                    }.onFailure {
                                        status = "Error: ${it.message ?: "unknown error"}"
                                    }
                                }
                            }
                        }
                    ) { Text("Send") }
                }
                OutlinedButton(onClick = {
                    if (ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
                        status = "Microphone ready — voice UI is next phase"
                    } else {
                        micLauncher.launch(Manifest.permission.RECORD_AUDIO)
                    }
                }) { Text("Enable Microphone") }
            }
        }
    }

    if (showSettings) {
        AlertDialog(
            onDismissRequest = { showSettings = false },
            title = { Text("Gemini API key") },
            text = {
                Column {
                    Text("Your key is stored using Android Keystore on this device. Do not commit it to GitHub.")
                    Spacer(Modifier.height(10.dp))
                    OutlinedTextField(value = draftKey, onValueChange = { draftKey = it }, singleLine = true)
                }
            },
            confirmButton = {
                Button(onClick = {
                    val clean = draftKey.trim()
                    if (clean.isNotEmpty()) {
                        secureStore.saveApiKey(clean)
                        apiKey = clean
                        status = "API key saved locally"
                    }
                    showSettings = false
                }) { Text("Save") }
            },
            dismissButton = {
                OutlinedButton(onClick = { showSettings = false }) { Text("Cancel") }
            }
        )
    }
}
