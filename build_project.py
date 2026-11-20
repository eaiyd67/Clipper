#!/usr/bin/env python3
"""
ClipPulse Android Project Generator
Generates all Gradle, AndroidManifest, XML resource, and Kotlin source files
for zero-PC compilation on GitHub Actions.
"""

import os

FILES = {}

# ==============================================================================
# 1. GRADLE & BUILD CONFIGURATION
# ==============================================================================

FILES["gradle.properties"] = r'''org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
'''

FILES["settings.gradle.kts"] = r'''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
        maven { url = uri("https://jitpack.io") }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://jitpack.io") }
    }
}

rootProject.name = "ClipPulse"
include(":app")
'''

FILES["build.gradle.kts"] = r'''plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
'''

FILES["app/build.gradle.kts"] = r'''plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.clippulse.studio"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.clippulse.studio"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
        }
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.core:core-ktx:1.13.1")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    implementation("androidx.media3:media3-exoplayer:1.4.1")
    implementation("androidx.media3:media3-ui:1.4.1")

    implementation("io.github.junkfood02.youtubedl-android:library:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:common:0.18.1")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
'''

FILES["app/proguard-rules.pro"] = r'''-keep class com.yausername.** { *; }
-dontwarn com.yausername.**
'''

# ==============================================================================
# 2. MANIFEST & XML RESOURCES
# ==============================================================================

FILES["app/src/main/AndroidManifest.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission
        android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />
    <uses-permission
        android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="29" />

    <application
        android:name=".ClipPulseApp"
        android:allowBackup="true"
        android:extractNativeLibs="true"
        android:icon="@drawable/ic_launcher"
        android:roundIcon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.ClipPulse"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.ClipExportService"
            android:enabled="true"
            android:exported="false"
            android:foregroundServiceType="dataSync" />

    </application>
</manifest>
'''

FILES["app/src/main/res/drawable/ic_launcher.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0B0B0F"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#16161D"
        android:pathData="M24,14h60a10,10 0 0 1 10,10v60a10,10 0 0 1 -10,10h-60a10,10 0 0 1 -10,-10v-60a10,10 0 0 1 10,-10z" />
    <path
        android:fillColor="#6366F1"
        android:pathData="M41,34L73,54L41,74Z" />
    <path
        android:strokeColor="#06B6D4"
        android:strokeWidth="4"
        android:strokeLineCap="round"
        android:pathData="M24,78L34,78L40,66L48,84L56,60L64,78L84,78" />
</vector>
'''

FILES["app/src/main/res/values/strings.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">ClipPulse</string>
</resources>
'''

FILES["app/src/main/res/values/themes.xml"] = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.ClipPulse" parent="android:Theme.Material.NoActionBar">
        <item name="android:windowBackground">#0B0B0F</item>
        <item name="android:statusBarColor">#0B0B0F</item>
        <item name="android:navigationBarColor">#0B0B0F</item>
    </style>
</resources>
'''

# ==============================================================================
# 3. APPLICATION & MAIN ACTIVITY
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/ClipPulseApp.kt"] = r'''package com.clippulse.studio

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import com.yausername.ffmpeg.FFmpeg
import com.yausername.youtubedl_android.YoutubeDL
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

class ClipPulseApp : Application() {

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        appScope.launch {
            ensureEnginesInitialized(applicationContext)
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                EXPORT_CHANNEL_ID,
                "ClipPulse Export Service",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Shows real-time progress while downloading and exporting video clips"
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }

    companion object {
        const val EXPORT_CHANNEL_ID = "clippulse_export_channel"
        private val appScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        private val initMutex = Mutex()

        @Volatile
        private var enginesReady = false

        suspend fun ensureEnginesInitialized(context: Context): Result<Unit> {
            if (enginesReady) return Result.success(Unit)
            return initMutex.withLock {
                if (enginesReady) return Result.success(Unit)
                runCatching {
                    YoutubeDL.getInstance().init(context.applicationContext)
                    FFmpeg.getInstance().init(context.applicationContext)
                    enginesReady = true
                }
            }
        }
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/MainActivity.kt"] = r'''package com.clippulse.studio

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.core.content.ContextCompat
import com.clippulse.studio.engine.TimeUtils
import com.clippulse.studio.ui.ClipPulseScreen
import com.clippulse.studio.ui.ClipPulseViewModel
import com.clippulse.studio.ui.theme.ClipPulseTheme

class MainActivity : ComponentActivity() {

    private val viewModel: ClipPulseViewModel by viewModels()

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { _ -> }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.parseColor("#0B0B0F")),
            navigationBarStyle = SystemBarStyle.dark(Color.parseColor("#0B0B0F"))
        )
        requestRuntimePermissions()
        handleIncomingIntent(intent)

        setContent {
            ClipPulseTheme {
                ClipPulseScreen(viewModel = viewModel)
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIncomingIntent(intent)
    }

    private fun handleIncomingIntent(intent: Intent?) {
        if (intent?.action == Intent.ACTION_SEND && intent.type == "text/plain") {
            val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
            val extracted = TimeUtils.extractUrlFromSharedText(sharedText)
            if (extracted.isNotBlank()) {
                viewModel.onUrlChanged(extracted)
            }
        }
    }

    private fun requestRuntimePermissions() {
        val needed = mutableListOf<String>()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
            ) {
                needed.add(Manifest.permission.POST_NOTIFICATIONS)
            }
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_VIDEO)
                != PackageManager.PERMISSION_GRANTED
            ) {
                needed.add(Manifest.permission.READ_MEDIA_VIDEO)
            }
        } else if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
            != PackageManager.PERMISSION_GRANTED
        ) {
            needed.add(Manifest.permission.READ_EXTERNAL_STORAGE)
        }

        if (needed.isNotEmpty()) {
            permissionLauncher.launch(needed.toTypedArray())
        }
    }
}
'''

# ==============================================================================
# 4. DOMAIN MODELS & DATA REPOSITORY
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/model/Models.kt"] = r'''package com.clippulse.studio.model

import java.util.UUID

enum class DetectionMode(val label: String, val subtitle: String) {
    ALL("All Signals", "Full multi-signal consensus scan"),
    HEATMAP("Most Replayed", "YouTube viewer replay spikes"),
    SUPER_CHAT("Super Chats", "RAM-safe live chat donor & reaction sync"),
    CHAT_HYPE("Chat Hype", "10s chat velocity & laughter spikes"),
    AUDIO_PEAK("Audio Peaks", "Waveform energy scanner for VODs & local files"),
    AI_VIRAL("AI Viral & Search", "Viral hook scoring or custom prompt search")
}

enum class SignalType(val label: String) {
    HEATMAP("Heatmap"),
    SUPER_CHAT("Super Chat"),
    CHAT_HYPE("Chat Hype"),
    AUDIO_PEAK("Audio Peak"),
    AI_PICK("AI Pick")
}

enum class AiProviderPreset(
    val displayName: String,
    val defaultBaseUrl: String,
    val defaultModel: String
) {
    DEEPSEEK(
        displayName = "DeepSeek",
        defaultBaseUrl = "https://api.deepseek.com/v1",
        defaultModel = "deepseek-chat"
    ),
    GEMINI(
        displayName = "Gemini",
        defaultBaseUrl = "https://generativelanguage.googleapis.com/v1beta/openai",
        defaultModel = "gemini-2.5-flash"
    ),
    OPENROUTER(
        displayName = "OpenRouter",
        defaultBaseUrl = "https://openrouter.ai/api/v1",
        defaultModel = "google/gemini-2.5-flash"
    ),
    CUSTOM(
        displayName = "Custom",
        defaultBaseUrl = "https://api.openai.com/v1",
        defaultModel = "gpt-4o-mini"
    )
}

data class AiSettings(
    val preset: AiProviderPreset = AiProviderPreset.DEEPSEEK,
    val baseUrl: String = AiProviderPreset.DEEPSEEK.defaultBaseUrl,
    val primaryApiKey: String = "",
    val backupApiKeys: List<String> = emptyList(),
    val selectedModel: String = AiProviderPreset.DEEPSEEK.defaultModel,
    val availableModels: List<String> = listOf(
        "deepseek-chat",
        "deepseek-reasoner",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gpt-4o-mini"
    ),
    val smartPeakOnly: Boolean = true,
    val offlineMode: Boolean = false
)

sealed interface AiConnectionState {
    data object Disconnected : AiConnectionState
    data object Testing : AiConnectionState
    data class Connected(val latencyMs: Long, val model: String) : AiConnectionState
    data class Error(val message: String) : AiConnectionState
}

data class HeatmapPoint(
    val startSec: Double,
    val endSec: Double,
    val value: Double
)

data class TranscriptSegment(
    val startSec: Double,
    val endSec: Double,
    val text: String
)

data class SuperChatEvent(
    val id: String = UUID.randomUUID().toString(),
    val authorName: String,
    val amountText: String,
    val amountNumeric: Double,
    val currency: String,
    val message: String,
    val offsetSec: Double,
    val isSticker: Boolean = false
)

data class ClipCandidate(
    val id: String = UUID.randomUUID().toString(),
    val title: String,
    val startSec: Double,
    val endSec: Double,
    val score: Int,
    val signals: List<SignalType>,
    val isMultiSignal: Boolean = false,
    val superChat: SuperChatEvent? = null,
    val transcriptSnippet: String = "",
    val reason: String = "",
    val selected: Boolean = true
) {
    val durationSec: Double
        get() = (endSec - startSec).coerceAtLeast(1.0)
}

data class VideoAnalysisResult(
    val sourceInput: String,
    val isLocalFile: Boolean,
    val localFilePath: String?,
    val title: String,
    val channelName: String,
    val durationSec: Double,
    val heatmap: List<HeatmapPoint>,
    val clips: List<ClipCandidate>,
    val transcriptCount: Int,
    val superChatCount: Int
)

data class ExportConfig(
    val useVerticalCrop: Boolean = false,
    val includeTxtSidecar: Boolean = true,
    val startPaddingSec: Int = 3,
    val endPaddingSec: Int = 5
)

data class ExportProgressState(
    val isExporting: Boolean = false,
    val currentIndex: Int = 0,
    val totalCount: Int = 0,
    val currentTitle: String = "",
    val fraction: Float = 0f,
    val statusMessage: String = "",
    val completedTitles: List<String> = emptyList(),
    val errorMessage: String? = null
)
'''

FILES["app/src/main/java/com/clippulse/studio/data/AiConfigRepository.kt"] = r'''package com.clippulse.studio.data

import android.content.Context
import com.clippulse.studio.model.AiProviderPreset
import com.clippulse.studio.model.AiSettings
import com.clippulse.studio.model.ExportConfig
import org.json.JSONArray

class AiConfigRepository(context: Context) {

    private val prefs = context.applicationContext.getSharedPreferences(
        "clippulse_prefs_v1",
        Context.MODE_PRIVATE
    )

    fun loadAiSettings(): AiSettings {
        val presetName = prefs.getString("ai_preset", AiProviderPreset.DEEPSEEK.name)
            ?: AiProviderPreset.DEEPSEEK.name
        val preset = runCatching { AiProviderPreset.valueOf(presetName) }
            .getOrDefault(AiProviderPreset.DEEPSEEK)

        val baseUrl = prefs.getString("ai_base_url", preset.defaultBaseUrl)
            ?: preset.defaultBaseUrl
        val primaryKey = prefs.getString("ai_primary_key", "") ?: ""
        val selectedModel = prefs.getString("ai_selected_model", preset.defaultModel)
            ?: preset.defaultModel
        val backupKeys = decodeStringList(prefs.getString("ai_backup_keys", "[]"))
        val availableModels = decodeStringList(prefs.getString("ai_available_models", "[]"))
            .ifEmpty {
                listOf(
                    "deepseek-chat",
                    "deepseek-reasoner",
                    "gemini-2.5-flash",
                    "gemini-2.5-pro",
                    "gpt-4o-mini"
                )
            }
        val smartPeakOnly = prefs.getBoolean("ai_smart_peak_only", true)
        val offlineMode = prefs.getBoolean("ai_offline_mode", false)

        return AiSettings(
            preset = preset,
            baseUrl = baseUrl,
            primaryApiKey = primaryKey,
            backupApiKeys = backupKeys,
            selectedModel = selectedModel,
            availableModels = availableModels,
            smartPeakOnly = smartPeakOnly,
            offlineMode = offlineMode
        )
    }

    fun saveAiSettings(settings: AiSettings) {
        prefs.edit()
            .putString("ai_preset", settings.preset.name)
            .putString("ai_base_url", settings.baseUrl.trim())
            .putString("ai_primary_key", settings.primaryApiKey.trim())
            .putString("ai_backup_keys", encodeStringList(settings.backupApiKeys))
            .putString("ai_selected_model", settings.selectedModel.trim())
            .putString("ai_available_models", encodeStringList(settings.availableModels))
            .putBoolean("ai_smart_peak_only", settings.smartPeakOnly)
            .putBoolean("ai_offline_mode", settings.offlineMode)
            .apply()
    }

    fun loadExportConfig(): ExportConfig {
        return ExportConfig(
            useVerticalCrop = prefs.getBoolean("export_vertical_crop", false),
            includeTxtSidecar = prefs.getBoolean("export_txt_sidecar", true),
            startPaddingSec = prefs.getInt("export_start_pad", 3),
            endPaddingSec = prefs.getInt("export_end_pad", 5)
        )
    }

    fun saveExportConfig(config: ExportConfig) {
        prefs.edit()
            .putBoolean("export_vertical_crop", config.useVerticalCrop)
            .putBoolean("export_txt_sidecar", config.includeTxtSidecar)
            .putInt("export_start_pad", config.startPaddingSec)
            .putInt("export_end_pad", config.endPaddingSec)
            .apply()
    }

    private fun encodeStringList(items: List<String>): String {
        val array = JSONArray()
        items.filter { it.isNotBlank() }.forEach { array.put(it.trim()) }
        return array.toString()
    }

    private fun decodeStringList(raw: String?): List<String> {
        if (raw.isNullOrBlank()) return emptyList()
        return runCatching {
            val array = JSONArray(raw)
            buildList {
                for (i in 0 until array.length()) {
                    val value = array.optString(i).trim()
                    if (value.isNotEmpty()) add(value)
                }
            }
        }.getOrDefault(emptyList())
    }
}
'''

# ==============================================================================
# 5. UNIVERSAL AI CLIENT (DYNAMIC FETCH, CONNECT, FAILOVER, STRICT JSON)
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/network/UniversalAiClient.kt"] = r'''package com.clippulse.studio.network

import android.os.SystemClock
import com.clippulse.studio.engine.TimeUtils
import com.clippulse.studio.model.AiSettings
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TranscriptSegment
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.util.Locale
import java.util.concurrent.TimeUnit

class UniversalAiClient {

    private val client = OkHttpClient.Builder()
        .connectTimeout(25, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    fun normalizeBaseUrl(rawUrl: String): String {
        var url = rawUrl.trim().trimEnd('/')
        if (url.endsWith("/chat/completions")) {
            url = url.removeSuffix("/chat/completions").trimEnd('/')
        }
        if (url.endsWith("/models")) {
            url = url.removeSuffix("/models").trimEnd('/')
        }
        return url
    }

    private fun orderedKeys(settings: AiSettings): List<String> {
        return buildList {
            if (settings.primaryApiKey.isNotBlank()) add(settings.primaryApiKey.trim())
            settings.backupApiKeys.forEach { key ->
                val trimmed = key.trim()
                if (trimmed.isNotEmpty() && !contains(trimmed)) add(trimmed)
            }
        }
    }

    suspend fun fetchModels(settings: AiSettings): Result<List<String>> = withContext(Dispatchers.IO) {
        val baseUrl = normalizeBaseUrl(settings.baseUrl)
        if (baseUrl.isBlank()) {
            return@withContext Result.failure(IllegalArgumentException("Base URL cannot be empty"))
        }
        val keys = orderedKeys(settings)
        if (keys.isEmpty()) {
            return@withContext Result.failure(IllegalArgumentException("Enter at least one API key first"))
        }

        var lastError = "Failed to fetch models"
        for (key in keys) {
            val request = Request.Builder()
                .url("$baseUrl/models")
                .addHeader("Authorization", "Bearer $key")
                .addHeader("Accept", "application/json")
                .get()
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    val bodyStr = response.body?.string().orEmpty()
                    if (!response.isSuccessful) {
                        lastError = parseHttpError(response.code, bodyStr)
                        if (shouldFailover(response.code)) continue
                        return@withContext Result.failure(IOException(lastError))
                    }

                    val models = parseModelsResponse(bodyStr)
                    if (models.isEmpty()) {
                        return@withContext Result.failure(
                            IOException("Endpoint returned 200 OK but no model IDs were found")
                        )
                    }
                    return@withContext Result.success(models)
                }
            } catch (e: Exception) {
                lastError = e.message ?: "Network error while fetching models"
            }
        }
        Result.failure(IOException(lastError))
    }

    suspend fun testConnection(settings: AiSettings): Result<Long> = withContext(Dispatchers.IO) {
        val baseUrl = normalizeBaseUrl(settings.baseUrl)
        if (baseUrl.isBlank()) {
            return@withContext Result.failure(IllegalArgumentException("Base URL is required"))
        }
        val model = settings.selectedModel.trim()
        if (model.isBlank()) {
            return@withContext Result.failure(IllegalArgumentException("Select or enter a model ID"))
        }
        val keys = orderedKeys(settings)
        if (keys.isEmpty()) {
            return@withContext Result.failure(IllegalArgumentException("API Key is required"))
        }

        val payload = JSONObject().apply {
            put("model", model)
            put("messages", JSONArray().apply {
                put(JSONObject().apply {
                    put("role", "user")
                    put("content", "ping")
                })
            })
            put("max_tokens", 1)
            put("temperature", 0)
        }

        var lastError = "Connection failed"
        for (key in keys) {
            val startMs = SystemClock.elapsedRealtime()
            val request = Request.Builder()
                .url("$baseUrl/chat/completions")
                .addHeader("Authorization", "Bearer $key")
                .addHeader("Content-Type", "application/json")
                .post(payload.toString().toRequestBody(jsonMediaType))
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    val bodyStr = response.body?.string().orEmpty()
                    val elapsed = (SystemClock.elapsedRealtime() - startMs).coerceAtLeast(1L)
                    if (!response.isSuccessful) {
                        lastError = parseHttpError(response.code, bodyStr)
                        if (shouldFailover(response.code)) continue
                        return@withContext Result.failure(IOException(lastError))
                    }
                    return@withContext Result.success(elapsed)
                }
            } catch (e: Exception) {
                lastError = e.message ?: "Network timeout or DNS error"
            }
        }
        Result.failure(IOException(lastError))
    }

    suspend fun alignSuperChats(
        settings: AiSettings,
        superChats: List<SuperChatEvent>,
        transcript: List<TranscriptSegment>,
        durationSec: Double
    ): Map<String, Pair<Double, Double>> = withContext(Dispatchers.IO) {
        if (settings.offlineMode || orderedKeys(settings).isEmpty() || superChats.isEmpty() || transcript.isEmpty()) {
            return@withContext emptyMap()
        }

        val targetEvents = superChats.take(15)
        val eventsSummary = buildString {
            targetEvents.forEach { sc ->
                val windowStart = (sc.offsetSec - 45.0).coerceAtLeast(0.0)
                val windowEnd = (sc.offsetSec + 75.0).coerceAtMost(durationSec)
                val nearbyLines = transcript.filter {
                    it.endSec >= windowStart && it.startSec <= windowEnd
                }.joinToString(" ") {
                    "[${String.format(Locale.US, "%.0f", it.startSec)}s] ${it.text}"
                }
                appendLine("ID=${sc.id} | ChatTime=${String.format(Locale.US, "%.0f", sc.offsetSec)}s | Donor=${sc.authorName} (${sc.amountText}) | Msg=${sc.message}")
                appendLine("TranscriptWindow: $nearbyLines")
                appendLine("---")
            }
        }

        val systemPrompt = """
You are a livestream clip timestamp aligner. Given Super Chat donations and surrounding transcript lines with timestamps in seconds, find the exact start_sec and end_sec when the streamer notices, reads, and reacts to each Super Chat.
Return STRICT JSON ONLY with no markdown fences, no commentary, and no thinking text:
{"alignments":[{"id":"...","start_sec":120.0,"end_sec":155.0}]}
        """.trimIndent()

        val rawResponse = sendChatCompletion(
            settings = settings,
            systemPrompt = systemPrompt,
            userPrompt = eventsSummary,
            maxTokens = 900
        ) ?: return@withContext emptyMap()

        val json = extractJsonObject(rawResponse) ?: return@withContext emptyMap()
        val array = json.optJSONArray("alignments") ?: return@withContext emptyMap()

        val result = mutableMapOf<String, Pair<Double, Double>>()
        for (i in 0 until array.length()) {
            val item = array.optJSONObject(i) ?: continue
            val id = item.optString("id")
            val start = item.optDouble("start_sec", Double.NaN)
            val end = item.optDouble("end_sec", Double.NaN)
            if (id.isNotBlank() && !start.isNaN() && !end.isNaN() && end > start) {
                result[id] = Pair(
                    start.coerceIn(0.0, durationSec),
                    end.coerceIn((start + 4.0).coerceAtMost(durationSec), durationSec)
                )
            }
        }
        result
    }

    suspend fun detectViralAndCustomClips(
        settings: AiSettings,
        videoTitle: String,
        durationSec: Double,
        transcript: List<TranscriptSegment>,
        anchorTimestampsSec: List<Double>,
        customQuery: String
    ): List<ClipCandidate> = withContext(Dispatchers.IO) {
        if (settings.offlineMode || orderedKeys(settings).isEmpty() || transcript.isEmpty()) {
            return@withContext emptyList()
        }

        val condensedTranscript = buildTokenOptimizedTranscript(
            transcript = transcript,
            durationSec = durationSec,
            anchorTimestampsSec = anchorTimestampsSec,
            smartPeakOnly = settings.smartPeakOnly
        )
        if (condensedTranscript.isBlank()) return@withContext emptyList()

        val taskDirective = if (customQuery.isNotBlank()) {
            "Find every moment matching the user's search query: \"$customQuery\". Score relevance and entertainment from 1 to 100."
        } else {
            "Identify the top 5-8 highest-retention viral hooks, funny moments, heated debates, or dramatic stories. Score viral potential from 1 to 100."
        }

        val systemPrompt = """
You are an expert short-form video editor. Analyze the timestamped transcript for "$videoTitle" (total duration ${String.format(Locale.US, "%.0f", durationSec)}s).
$taskDirective
Each clip should be 15 to 60 seconds long with clean start_sec and end_sec boundaries.
Return STRICT JSON ONLY with no markdown fences, no prose, and no thinking text:
{"clips":[{"title":"Hooky 5-word title","start_sec":42.0,"end_sec":78.0,"score":92,"reason":"Why this moment hooks viewers"}]}
        """.trimIndent()

        val rawResponse = sendChatCompletion(
            settings = settings,
            systemPrompt = systemPrompt,
            userPrompt = condensedTranscript,
            maxTokens = 1200
        ) ?: return@withContext emptyList()

        val json = extractJsonObject(rawResponse) ?: return@withContext emptyList()
        val array = json.optJSONArray("clips") ?: return@withContext emptyList()

        buildList {
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                val rawStart = item.optDouble("start_sec", Double.NaN)
                val rawEnd = item.optDouble("end_sec", Double.NaN)
                if (rawStart.isNaN() || rawEnd.isNaN() || rawEnd <= rawStart) continue

                val start = rawStart.coerceIn(0.0, (durationSec - 3.0).coerceAtLeast(0.0))
                val end = rawEnd.coerceIn(start + 3.0, durationSec)
                val title = item.optString("title").ifBlank {
                    "AI Highlight @ ${TimeUtils.formatTimestamp(start)}"
                }
                val score = item.optInt("score", 82).coerceIn(1, 100)
                val reason = item.optString("reason")
                val snippet = transcript.filter { it.endSec >= start && it.startSec <= end }
                    .joinToString(" ") { it.text }
                    .take(260)

                add(
                    ClipCandidate(
                        title = title,
                        startSec = start,
                        endSec = end,
                        score = score,
                        signals = listOf(SignalType.AI_PICK),
                        transcriptSnippet = snippet,
                        reason = reason
                    )
                )
            }
        }
    }

    private fun buildTokenOptimizedTranscript(
        transcript: List<TranscriptSegment>,
        durationSec: Double,
        anchorTimestampsSec: List<Double>,
        smartPeakOnly: Boolean
    ): String {
        val windows: List<Pair<Double, Double>> = if (smartPeakOnly && anchorTimestampsSec.isNotEmpty()) {
            val rawWindows = anchorTimestampsSec.sorted().map { anchor ->
                Pair(
                    (anchor - 60.0).coerceAtLeast(0.0),
                    (anchor + 60.0).coerceAtMost(durationSec)
                )
            }
            mergeWindows(rawWindows)
        } else if (smartPeakOnly && durationSec > 600.0) {
            val step = durationSec / 5.0
            (0 until 5).map { idx ->
                val center = (idx + 0.5) * step
                Pair(
                    (center - 60.0).coerceAtLeast(0.0),
                    (center + 60.0).coerceAtMost(durationSec)
                )
            }
        } else {
            listOf(Pair(0.0, durationSec))
        }

        val sb = StringBuilder()
        for ((wStart, wEnd) in windows) {
            sb.appendLine("--- Window ${TimeUtils.formatTimestamp(wStart)} to ${TimeUtils.formatTimestamp(wEnd)} ---")
            val segs = transcript.filter { it.endSec >= wStart && it.startSec <= wEnd }
            for (seg in segs) {
                if (sb.length > 14_000) break
                sb.append('[')
                sb.append(String.format(Locale.US, "%.0f", seg.startSec))
                sb.append("s] ")
                sb.appendLine(seg.text)
            }
            if (sb.length > 14_000) break
        }
        return sb.toString()
    }

    private fun mergeWindows(sortedWindows: List<Pair<Double, Double>>): List<Pair<Double, Double>> {
        if (sortedWindows.isEmpty()) return emptyList()
        val merged = mutableListOf(sortedWindows.first())
        for (i in 1 until sortedWindows.size) {
            val prev = merged.last()
            val curr = sortedWindows[i]
            if (curr.first <= prev.second + 15.0) {
                merged[merged.lastIndex] = Pair(prev.first, maxOf(prev.second, curr.second))
            } else {
                merged.add(curr)
            }
        }
        return merged
    }

    private fun sendChatCompletion(
        settings: AiSettings,
        systemPrompt: String,
        userPrompt: String,
        maxTokens: Int
    ): String? {
        val baseUrl = normalizeBaseUrl(settings.baseUrl)
        val keys = orderedKeys(settings)
        if (baseUrl.isBlank() || keys.isEmpty()) return null

        val payload = JSONObject().apply {
            put("model", settings.selectedModel)
            put("messages", JSONArray().apply {
                put(JSONObject().apply {
                    put("role", "system")
                    put("content", systemPrompt)
                })
                put(JSONObject().apply {
                    put("role", "user")
                    put("content", userPrompt)
                })
            })
            put("max_tokens", maxTokens)
            put("temperature", 0.2)
        }

        for (key in keys) {
            val request = Request.Builder()
                .url("$baseUrl/chat/completions")
                .addHeader("Authorization", "Bearer $key")
                .addHeader("Content-Type", "application/json")
                .post(payload.toString().toRequestBody(jsonMediaType))
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    val bodyStr = response.body?.string().orEmpty()
                    if (!response.isSuccessful) {
                        if (shouldFailover(response.code)) continue
                        return null
                    }
                    val root = JSONObject(bodyStr)
                    val choices = root.optJSONArray("choices") ?: return null
                    if (choices.length() == 0) return null
                    val message = choices.getJSONObject(0).optJSONObject("message") ?: return null
                    return message.optString("content")
                }
            } catch (_: Exception) {
                // Fail over to next backup key on transient network failure
            }
        }
        return null
    }

    private fun extractJsonObject(rawText: String): JSONObject? {
        val cleaned = rawText
            .replace(Regex("<think>[\\s\\S]*?</think>", RegexOption.IGNORE_CASE), "")
            .replace("```json", "")
            .replace("```", "")
            .trim()

        runCatching { return JSONObject(cleaned) }

        val match = Regex("\\{[\\s\\S]*\\}").find(cleaned) ?: return null
        return runCatching { JSONObject(match.value) }.getOrNull()
    }

    private fun parseModelsResponse(bodyStr: String): List<String> {
        val root = JSONObject(bodyStr)
        val dataArray = root.optJSONArray("data") ?: root.optJSONArray("models") ?: return emptyList()
        return buildList {
            for (i in 0 until dataArray.length()) {
                val obj = dataArray.optJSONObject(i)
                val id = obj?.optString("id")?.ifBlank { obj.optString("name") }
                    ?: dataArray.optString(i)
                if (id.isNotBlank()) add(id.removePrefix("models/"))
            }
        }.distinct().sorted()
    }

    private fun shouldFailover(httpCode: Int): Boolean {
        return httpCode == 401 || httpCode == 403 || httpCode == 429 || httpCode >= 500
    }

    private fun parseHttpError(code: Int, body: String): String {
        val parsedMsg = runCatching {
            val json = JSONObject(body)
            json.optJSONObject("error")?.optString("message")
                ?.ifBlank { json.optString("message") }
        }.getOrNull()

        return if (!parsedMsg.isNullOrBlank()) {
            "HTTP $code: $parsedMsg"
        } else {
            "HTTP $code: ${body.take(140).ifBlank { "Request rejected by API server" }}"
        }
    }
}
'''

# ==============================================================================
# 6. CORE ENGINE: TIME UTILS, FFMPEG RUNNER, STREAMING PARSER, CONSENSUS, ANALYZER, EXPORTER
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/engine/TimeUtils.kt"] = r'''package com.clippulse.studio.engine

import java.util.Locale

object TimeUtils {

    fun formatTimestamp(totalSeconds: Double): String {
        val safe = totalSeconds.coerceAtLeast(0.0).toLong()
        val hours = safe / 3600L
        val minutes = (safe % 3600L) / 60L
        val seconds = safe % 60L
        return if (hours > 0L) {
            String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds)
        } else {
            String.format(Locale.US, "%02d:%02d", minutes, seconds)
        }
    }

    fun formatFfmpegTimestamp(totalSeconds: Double): String {
        val safe = totalSeconds.coerceAtLeast(0.0)
        val wholeSec = safe.toLong()
        val hours = wholeSec / 3600L
        val minutes = (wholeSec % 3600L) / 60L
        val seconds = wholeSec % 60L
        return String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds)
    }

    fun formatDownloadSection(startSec: Double, endSec: Double): String {
        val startStr = formatFfmpegTimestamp(startSec)
        val endStr = formatFfmpegTimestamp(endSec.coerceAtLeast(startSec + 1.0))
        return "*$startStr-$endStr"
    }

    fun parseVttTimestamp(raw: String): Double {
        val cleaned = raw.trim().replace(',', '.')
        val parts = cleaned.split(':')
        return when (parts.size) {
            3 -> {
                val h = parts[0].toDoubleOrNull() ?: 0.0
                val m = parts[1].toDoubleOrNull() ?: 0.0
                val s = parts[2].toDoubleOrNull() ?: 0.0
                h * 3600.0 + m * 60.0 + s
            }
            2 -> {
                val m = parts[0].toDoubleOrNull() ?: 0.0
                val s = parts[1].toDoubleOrNull() ?: 0.0
                m * 60.0 + s
            }
            else -> 0.0
        }
    }

    fun extractUrlFromSharedText(text: String): String {
        val urlRegex = Regex("https?://[\\w\\-._~:/?#\\[\\]@!$&'()*+,;=%]+")
        return urlRegex.find(text)?.value ?: text.trim()
    }

    fun sanitizeFileName(raw: String): String {
        return raw.replace(Regex("[^a-zA-Z0-9._ -]"), "_")
            .replace(Regex("\\s+"), "_")
            .trim('_')
            .take(64)
            .ifBlank { "ClipPulse_Clip" }
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/engine/FfmpegRunner.kt"] = r'''package com.clippulse.studio.engine

import android.content.Context
import android.media.MediaMetadataRetriever
import android.net.Uri
import com.clippulse.studio.ClipPulseApp
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalType
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.util.Locale

class FfmpegRunner(private val context: Context) {

    data class FfmpegResult(
        val exitCode: Int,
        val output: String
    )

    private fun resolveFfmpegBinary(): File? {
        val candidates = listOf(
            File(context.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/bin/ffmpeg"),
            File(context.filesDir, "youtubedl-android/packages/ffmpeg/usr/bin/ffmpeg"),
            File(context.applicationInfo.nativeLibraryDir, "libffmpeg.so")
        )
        return candidates.firstOrNull { it.exists() && it.canExecute() }
            ?: candidates.firstOrNull { it.exists() }
    }

    private fun buildLibraryPath(): String {
        val paths = listOf(
            File(context.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/lib").absolutePath,
            File(context.noBackupFilesDir, "youtubedl-android/packages/python/usr/lib").absolutePath,
            File(context.filesDir, "youtubedl-android/packages/ffmpeg/usr/lib").absolutePath,
            context.applicationInfo.nativeLibraryDir
        )
        return paths.joinToString(":")
    }

    suspend fun execute(args: List<String>): FfmpegResult = withContext(Dispatchers.IO) {
        ClipPulseApp.ensureEnginesInitialized(context)
        val binary = resolveFfmpegBinary()
            ?: return@withContext FfmpegResult(-1, "FFmpeg binary not found in native libraries")

        val cmd = listOf(binary.absolutePath) + args
        val pb = ProcessBuilder(cmd).redirectErrorStream(true)
        val env = pb.environment()
        val existingLd = env["LD_LIBRARY_PATH"].orEmpty()
        val customLd = buildLibraryPath()
        env["LD_LIBRARY_PATH"] = if (existingLd.isNotBlank()) "$customLd:$existingLd" else customLd

        runCatching {
            val process = pb.start()
            val out = StringBuilder()
            BufferedReader(InputStreamReader(process.inputStream)).use { reader ->
                var line: String?
                while (reader.readLine().also { line = it } != null) {
                    out.appendLine(line)
                }
            }
            val code = process.waitFor()
            FfmpegResult(code, out.toString())
        }.getOrElse { err ->
            FfmpegResult(-1, err.message ?: "FFmpeg execution error")
        }
    }

    suspend fun copyUriToCache(uri: Uri, targetFile: File): Result<File> = withContext(Dispatchers.IO) {
        runCatching {
            targetFile.parentFile?.mkdirs()
            context.contentResolver.openInputStream(uri)?.use { input ->
                targetFile.outputStream().use { output ->
                    input.copyTo(output, bufferSize = 65536)
                }
            } ?: error("Unable to open selected video URI")
            targetFile
        }
    }

    fun probeLocalDurationSec(filePath: String): Double {
        val retriever = MediaMetadataRetriever()
        return try {
            retriever.setDataSource(filePath)
            val ms = retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)
                ?.toLongOrNull() ?: 0L
            (ms / 1000.0).coerceAtLeast(1.0)
        } catch (_: Exception) {
            60.0
        } finally {
            runCatching { retriever.release() }
        }
    }

    suspend fun scanAudioEnergyPeaks(
        inputPath: String,
        durationSec: Double
    ): List<ClipCandidate> = withContext(Dispatchers.IO) {
        val result = execute(
            listOf(
                "-hide_banner",
                "-nostats",
                "-i", inputPath,
                "-vn",
                "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
                "-f", "null",
                "-"
            )
        )

        val rmsBySec = mutableListOf<Pair<Double, Double>>()
        var currentTime = 0.0
        val ptsRegex = Regex("pts_time:([0-9.]+)")
        val rmsRegex = Regex("RMS_level=(-?[0-9.]+)")

        for (line in result.output.lineSequence()) {
            val ptsMatch = ptsRegex.find(line)
            if (ptsMatch != null) {
                currentTime = ptsMatch.groupValues[1].toDoubleOrNull() ?: currentTime
                continue
            }
            val rmsMatch = rmsRegex.find(line)
            if (rmsMatch != null) {
                val db = rmsMatch.groupValues[1].toDoubleOrNull()
                if (db != null && db.isFinite() && db > -90.0) {
                    rmsBySec.add(Pair(currentTime, db))
                }
            }
        }

        if (rmsBySec.size < 6) {
            val windowCount = (durationSec / 90.0).toInt().coerceIn(2, 6)
            val step = durationSec / (windowCount + 1)
            return@withContext (1..windowCount).map { idx ->
                val center = idx * step
                val start = (center - 15.0).coerceAtLeast(0.0)
                val end = (center + 15.0).coerceAtMost(durationSec)
                ClipCandidate(
                    title = "Highlight Segment #$idx",
                    startSec = start,
                    endSec = end,
                    score = 72,
                    signals = listOf(SignalType.AUDIO_PEAK),
                    reason = "Key visual segment candidate"
                )
            }
        }

        val meanDb = rmsBySec.map { it.second }.average()
        val stdDb = kotlin.math.sqrt(
            rmsBySec.map { (it.second - meanDb) * (it.second - meanDb) }.average()
        ).coerceAtLeast(1.5)

        val spikes = rmsBySec
            .filter { it.second > meanDb + 1.15 * stdDb }
            .sortedByDescending { it.second }

        val picked = mutableListOf<ClipCandidate>()
        for ((sec, db) in spikes) {
            if (picked.size >= 8) break
            if (picked.any { kotlin.math.abs(it.startSec - (sec - 12.0)) < 22.0 }) continue
            val start = (sec - 12.0).coerceAtLeast(0.0)
            val end = (sec + 18.0).coerceAtMost(durationSec)
            val z = ((db - meanDb) / stdDb).coerceIn(1.0, 4.0)
            val score = (70 + (z * 7.5)).toInt().coerceIn(68, 97)
            picked.add(
                ClipCandidate(
                    title = "Audio Energy Spike @ ${TimeUtils.formatTimestamp(sec)}",
                    startSec = start,
                    endSec = end,
                    score = score,
                    signals = listOf(SignalType.AUDIO_PEAK),
                    reason = String.format(
                        Locale.US,
                        "Vocal/SFX surge (%.1f dB vs %.1f dB avg)",
                        db,
                        meanDb
                    )
                )
            )
        }
        picked.sortedBy { it.startSec }
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/engine/ChatAndSubtitleParser.kt"] = r'''package com.clippulse.studio.engine

import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TranscriptSegment
import org.json.JSONObject
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets
import java.util.Locale
import kotlin.math.sqrt

object ChatAndSubtitleParser {

    data class LiveChatScanResult(
        val superChats: List<SuperChatEvent>,
        val velocityClips: List<ClipCandidate>,
        val totalMessagesScanned: Int
    )

    fun streamParseLiveChat(
        chatFile: File,
        durationSec: Double,
        minDonationUsdEquivalent: Double = 0.0
    ): LiveChatScanResult {
        if (!chatFile.exists() || chatFile.length() == 0L) {
            return LiveChatScanResult(emptyList(), emptyList(), 0)
        }

        val superChats = mutableListOf<SuperChatEvent>()
        val bucketCounts = HashMap<Int, Int>()
        val bucketSampleMessages = HashMap<Int, MutableList<String>>()
        var totalMessages = 0

        BufferedReader(
            InputStreamReader(FileInputStream(chatFile), StandardCharsets.UTF_8),
            65536
        ).use { reader ->
            var line: String?
            while (reader.readLine().also { line = it } != null) {
                val trimmed = line?.trim().orEmpty()
                if (trimmed.isEmpty() || !trimmed.startsWith("{")) continue

                runCatching {
                    val root = JSONObject(trimmed)
                    val replayAction = root.optJSONObject("replayChatItemAction") ?: return@runCatching
                    val offsetMs = replayAction.optString("videoOffsetTimeMsec").toDoubleOrNull()
                        ?: replayAction.optDouble("videoOffsetTimeMsec", Double.NaN)
                    if (offsetMs.isNaN() || offsetMs < 0.0) return@runCatching

                    val offsetSec = offsetMs / 1000.0
                    if (durationSec > 0.0 && offsetSec > durationSec + 30.0) return@runCatching

                    val actions = replayAction.optJSONArray("actions") ?: return@runCatching
                    for (i in 0 until actions.length()) {
                        val action = actions.optJSONObject(i) ?: continue
                        val addItem = action.optJSONObject("addChatItemAction") ?: continue
                        val item = addItem.optJSONObject("item") ?: continue

                        val textRenderer = item.optJSONObject("liveChatTextMessageRenderer")
                        if (textRenderer != null) {
                            totalMessages++
                            val bucket = (offsetSec / 10.0).toInt()
                            bucketCounts[bucket] = (bucketCounts[bucket] ?: 0) + 1
                            val msg = extractRunsText(textRenderer.optJSONObject("message"))
                            if (msg.isNotBlank()) {
                                val samples = bucketSampleMessages.getOrPut(bucket) { mutableListOf() }
                                if (samples.size < 3) samples.add(msg.take(60))
                            }
                        }

                        val paidMsg = item.optJSONObject("liveChatPaidMessageRenderer")
                        if (paidMsg != null) {
                            totalMessages++
                            val bucket = (offsetSec / 10.0).toInt()
                            bucketCounts[bucket] = (bucketCounts[bucket] ?: 0) + 3

                            val author = extractSimpleOrRunsText(paidMsg.optJSONObject("authorName"))
                                .ifBlank { "Supporter" }
                            val amountRaw = extractSimpleOrRunsText(paidMsg.optJSONObject("purchaseAmountText"))
                            val (currency, numeric) = parseCurrencyAmount(amountRaw)
                            val message = extractRunsText(paidMsg.optJSONObject("message"))

                            if (numeric >= minDonationUsdEquivalent) {
                                superChats.add(
                                    SuperChatEvent(
                                        authorName = author,
                                        amountText = amountRaw.ifBlank { "$5.00" },
                                        amountNumeric = numeric,
                                        currency = currency,
                                        message = message,
                                        offsetSec = offsetSec,
                                        isSticker = false
                                    )
                                )
                            }
                        }

                        val sticker = item.optJSONObject("liveChatPaidStickerRenderer")
                        if (sticker != null) {
                            totalMessages++
                            val bucket = (offsetSec / 10.0).toInt()
                            bucketCounts[bucket] = (bucketCounts[bucket] ?: 0) + 3

                            val author = extractSimpleOrRunsText(sticker.optJSONObject("authorName"))
                                .ifBlank { "Supporter" }
                            val amountRaw = extractSimpleOrRunsText(sticker.optJSONObject("purchaseAmountText"))
                            val (currency, numeric) = parseCurrencyAmount(amountRaw)
                            val stickerLabel = sticker.optJSONObject("sticker")
                                ?.optJSONObject("accessibility")
                                ?.optJSONObject("accessibilityData")
                                ?.optString("label")
                                .orEmpty()
                                .ifBlank { "Super Sticker" }

                            if (numeric >= minDonationUsdEquivalent) {
                                superChats.add(
                                    SuperChatEvent(
                                        authorName = author,
                                        amountText = amountRaw.ifBlank { "$5.00" },
                                        amountNumeric = numeric,
                                        currency = currency,
                                        message = stickerLabel,
                                        offsetSec = offsetSec,
                                        isSticker = true
                                    )
                                )
                            }
                        }
                    }
                }
            }
        }

        val velocityClips = buildVelocitySpikeClips(
            bucketCounts = bucketCounts,
            bucketSamples = bucketSampleMessages,
            durationSec = durationSec
        )

        return LiveChatScanResult(
            superChats = superChats.sortedBy { it.offsetSec },
            velocityClips = velocityClips,
            totalMessagesScanned = totalMessages
        )
    }

    private fun buildVelocitySpikeClips(
        bucketCounts: Map<Int, Int>,
        bucketSamples: Map<Int, List<String>>,
        durationSec: Double
    ): List<ClipCandidate> {
        if (bucketCounts.size < 4) return emptyList()

        val values = bucketCounts.values.map { it.toDouble() }
        val mean = values.average()
        val stdDev = sqrt(values.map { (it - mean) * (it - mean) }.average()).coerceAtLeast(1.0)
        val threshold = mean + 1.8 * stdDev

        val topBuckets = bucketCounts.entries
            .filter { it.value >= threshold && it.value >= 4 }
            .sortedByDescending { it.value }

        val clips = mutableListOf<ClipCandidate>()
        for ((bucket, count) in topBuckets) {
            if (clips.size >= 10) break
            val centerSec = bucket * 10.0 + 5.0
            if (clips.any { kotlin.math.abs(((it.startSec + it.endSec) / 2.0) - centerSec) < 25.0 }) {
                continue
            }
            val start = (centerSec - 14.0).coerceAtLeast(0.0)
            val end = if (durationSec > 0.0) {
                (centerSec + 18.0).coerceAtMost(durationSec)
            } else {
                centerSec + 18.0
            }
            val zScore = ((count - mean) / stdDev).coerceIn(1.5, 5.0)
            val hypeScore = (72 + (zScore * 5.5)).toInt().coerceIn(70, 98)
            val sampleText = bucketSamples[bucket]?.joinToString(" | ").orEmpty()

            clips.add(
                ClipCandidate(
                    title = "Chat Hype Surge (${count} msgs/10s)",
                    startSec = start,
                    endSec = end,
                    score = hypeScore,
                    signals = listOf(SignalType.CHAT_HYPE),
                    transcriptSnippet = sampleText,
                    reason = String.format(
                        Locale.US,
                        "Chat velocity hit %d msgs/10s (%.1fx average)",
                        count,
                        count / mean.coerceAtLeast(1.0)
                    )
                )
            )
        }
        return clips.sortedBy { it.startSec }
    }

    fun parseSubtitleFile(subFile: File): List<TranscriptSegment> {
        if (!subFile.exists() || subFile.length() == 0L) return emptyList()

        val segments = mutableListOf<TranscriptSegment>()
        var currentStart = -1.0
        var currentEnd = -1.0
        val currentText = StringBuilder()
        var lastCleanLine = ""

        BufferedReader(
            InputStreamReader(FileInputStream(subFile), StandardCharsets.UTF_8),
            32768
        ).use { reader ->
            var line: String?
            while (reader.readLine().also { line = it } != null) {
                val raw = line?.trim().orEmpty()
                if (raw.contains("-->")) {
                    if (currentStart >= 0.0 && currentText.isNotEmpty()) {
                        val clean = cleanCaptionText(currentText.toString())
                        if (clean.isNotBlank() && clean != lastCleanLine) {
                            segments.add(TranscriptSegment(currentStart, currentEnd, clean))
                            lastCleanLine = clean
                        }
                    }
                    currentText.clear()
                    val times = raw.split("-->")
                    currentStart = TimeUtils.parseVttTimestamp(times[0].trim().split(" ").first())
                    currentEnd = TimeUtils.parseVttTimestamp(times[1].trim().split(" ").first())
                } else if (
                    raw.isNotEmpty() &&
                    !raw.startsWith("WEBVTT") &&
                    !raw.startsWith("Kind:") &&
                    !raw.startsWith("Language:") &&
                    raw.toIntOrNull() == null &&
                    currentStart >= 0.0
                ) {
                    if (currentText.isNotEmpty()) currentText.append(' ')
                    currentText.append(raw)
                }
            }
        }

        if (currentStart >= 0.0 && currentText.isNotEmpty()) {
            val clean = cleanCaptionText(currentText.toString())
            if (clean.isNotBlank() && clean != lastCleanLine) {
                segments.add(TranscriptSegment(currentStart, currentEnd, clean))
            }
        }
        return segments
    }

    private fun cleanCaptionText(raw: String): String {
        return raw.replace(Regex("<[^>]+>"), "")
            .replace("&amp;", "&")
            .replace("&quot;", "\"")
            .replace("&#39;", "'")
            .replace(Regex("\\s+"), " ")
            .trim()
    }

    private fun extractSimpleOrRunsText(obj: JSONObject?): String {
        if (obj == null) return ""
        val simple = obj.optString("simpleText")
        if (simple.isNotBlank()) return simple
        return extractRunsText(obj)
    }

    private fun extractRunsText(obj: JSONObject?): String {
        if (obj == null) return ""
        val runs = obj.optJSONArray("runs") ?: return obj.optString("simpleText")
        val sb = StringBuilder()
        for (i in 0 until runs.length()) {
            val part = runs.optJSONObject(i) ?: continue
            val text = part.optString("text")
            if (text.isNotEmpty()) {
                sb.append(text)
            } else {
                val emoji = part.optJSONObject("emoji")?.optJSONArray("shortcuts")?.optString(0)
                if (!emoji.isNullOrBlank()) sb.append(emoji)
            }
        }
        return sb.toString().trim()
    }

    private fun parseCurrencyAmount(raw: String): Pair<String, Double> {
        val cleaned = raw.trim()
        val currency = cleaned.takeWhile { !it.isDigit() && it != '.' && it != ',' }
            .trim()
            .ifBlank { "$" }
        val numStr = cleaned.replace(Regex("[^0-9.]"), "")
        val amount = numStr.toDoubleOrNull() ?: 0.0
        return Pair(currency, amount)
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/engine/ConsensusEngine.kt"] = r'''package com.clippulse.studio.engine

import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalType

object ConsensusEngine {

    fun mergeAndRank(
        candidates: List<ClipCandidate>,
        mergeGapSec: Double = 18.0
    ): List<ClipCandidate> {
        if (candidates.isEmpty()) return emptyList()

        val sorted = candidates.sortedBy { it.startSec }
        val merged = mutableListOf<ClipCandidate>()

        for (next in sorted) {
            if (merged.isEmpty()) {
                merged.add(next)
                continue
            }

            val current = merged.last()
            val overlapsOrClose = next.startSec <= (current.endSec + mergeGapSec)

            if (overlapsOrClose) {
                val combinedSignals = (current.signals + next.signals).distinct()
                val isMulti = combinedSignals.size >= 2
                val baseMax = maxOf(current.score, next.score)
                val boostedScore = if (isMulti) {
                    (baseMax + (combinedSignals.size - 1) * 9).coerceAtMost(100)
                } else {
                    baseMax
                }

                val preferredSuperChat = current.superChat ?: next.superChat
                val preferredTitle = when {
                    preferredSuperChat != null ->
                        "${preferredSuperChat.amountText} Super Chat • ${preferredSuperChat.authorName}"
                    current.signals.contains(SignalType.AI_PICK) -> current.title
                    next.signals.contains(SignalType.AI_PICK) -> next.title
                    current.score >= next.score -> current.title
                    else -> next.title
                }
                val combinedSnippet = listOf(current.transcriptSnippet, next.transcriptSnippet)
                    .filter { it.isNotBlank() }
                    .distinct()
                    .joinToString(" • ")
                    .take(300)

                val combinedReason = listOf(current.reason, next.reason)
                    .filter { it.isNotBlank() }
                    .distinct()
                    .joinToString(" + ")

                merged[merged.lastIndex] = current.copy(
                    title = preferredTitle,
                    startSec = minOf(current.startSec, next.startSec),
                    endSec = maxOf(current.endSec, next.endSec),
                    score = boostedScore,
                    signals = combinedSignals,
                    isMultiSignal = isMulti,
                    superChat = preferredSuperChat,
                    transcriptSnippet = combinedSnippet,
                    reason = combinedReason
                )
            } else {
                merged.add(next)
            }
        }

        return merged.sortedWith(
            compareByDescending<ClipCandidate> { it.isMultiSignal }
                .thenByDescending { it.score }
                .thenBy { it.startSec }
        )
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/engine/VideoAnalysisEngine.kt"] = r'''package com.clippulse.studio.engine

import android.content.Context
import android.net.Uri
import com.clippulse.studio.ClipPulseApp
import com.clippulse.studio.model.AiSettings
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.HeatmapPoint
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.model.TranscriptSegment
import com.clippulse.studio.model.VideoAnalysisResult
import com.clippulse.studio.network.UniversalAiClient
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.util.Locale

class VideoAnalysisEngine(
    private val context: Context,
    private val aiClient: UniversalAiClient,
    private val ffmpegRunner: FfmpegRunner
) {

    suspend fun analyzeRemoteUrl(
        url: String,
        mode: DetectionMode,
        aiSettings: AiSettings,
        minSuperChatUsd: Double,
        customAiPrompt: String,
        onProgress: (String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        runCatching {
            onProgress("Initializing yt-dlp & FFmpeg engines...")
            ClipPulseApp.ensureEnginesInitialized(context).getOrThrow()

            val workDir = File(context.cacheDir, "analysis_${System.currentTimeMillis()}").apply {
                mkdirs()
            }

            onProgress("Fetching metadata, heatmap & live chat (zero video download)...")
            val request = YoutubeDLRequest(url).apply {
                addOption("--skip-download")
                addOption("--write-info-json")
                addOption("--write-auto-sub")
                addOption("--write-subs")
                addOption("--sub-langs", "en.*,live_chat")
                addOption("--no-playlist")
                addOption("--no-warnings")
                addOption("-o", File(workDir, "source").absolutePath)
            }

            val ytResponse = YoutubeDL.getInstance().execute(request) { _, _, line ->
                if (line != null && (line.contains("Writing") || line.contains("Downloading"))) {
                    onProgress(line.take(72))
                }
            }

            val infoFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".info.json") }
                ?: error("Could not retrieve video metadata. Verify the link or update yt-dlp in settings.\n${ytResponse.err.take(180)}")

            val infoJson = JSONObject(infoFile.readText())
            val title = infoJson.optString("title").ifBlank { "Untitled Video" }
            val channel = infoJson.optString("uploader")
                .ifBlank { infoJson.optString("channel").ifBlank { "Creator" } }
            val durationSec = infoJson.optDouble("duration", 0.0).coerceAtLeast(1.0)

            onProgress("Parsing viewer replay heatmap curve...")
            val heatmap = parseHeatmap(infoJson)

            onProgress("Parsing timed transcript captions...")
            val subFiles = workDir.listFiles()?.filter {
                it.name.endsWith(".vtt") || it.name.endsWith(".srt")
            }.orEmpty()
            val transcript = subFiles
                .sortedBy { if (it.name.contains(".en.")) 0 else 1 }
                .firstOrNull()
                ?.let { ChatAndSubtitleParser.parseSubtitleFile(it) }
                .orEmpty()

            onProgress("Stream-scanning live chat & Super Chats...")
            val chatFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".live_chat.json") }
            val chatScan = if (chatFile != null) {
                ChatAndSubtitleParser.streamParseLiveChat(
                    chatFile = chatFile,
                    durationSec = durationSec,
                    minDonationUsdEquivalent = minSuperChatUsd
                )
            } else {
                ChatAndSubtitleParser.LiveChatScanResult(emptyList(), emptyList(), 0)
            }

            val allCandidates = mutableListOf<ClipCandidate>()

            if (mode == DetectionMode.ALL || mode == DetectionMode.HEATMAP) {
                allCandidates += extractHeatmapClips(heatmap, transcript, durationSec)
            }

            if ((mode == DetectionMode.ALL || mode == DetectionMode.SUPER_CHAT) && chatScan.superChats.isNotEmpty()) {
                onProgress("Aligning ${chatScan.superChats.size} Super Chats with streamer reactions...")
                val alignments = aiClient.alignSuperChats(
                    settings = aiSettings,
                    superChats = chatScan.superChats,
                    transcript = transcript,
                    durationSec = durationSec
                )

                for (sc in chatScan.superChats) {
                    val aligned = alignments[sc.id]
                    val start = aligned?.first ?: (sc.offsetSec - 4.0).coerceAtLeast(0.0)
                    val end = aligned?.second ?: (sc.offsetSec + 26.0).coerceAtMost(durationSec)
                    val snippet = transcript.filter { it.endSec >= start && it.startSec <= end }
                        .joinToString(" ") { it.text }
                        .take(240)
                    val donationBoost = (sc.amountNumeric.coerceAtMost(100.0) * 0.25).toInt()
                    val score = (76 + donationBoost).coerceIn(75, 100)

                    allCandidates.add(
                        ClipCandidate(
                            title = "${sc.amountText} Super Chat • ${sc.authorName}",
                            startSec = start,
                            endSec = end,
                            score = score,
                            signals = listOf(SignalType.SUPER_CHAT),
                            superChat = sc,
                            transcriptSnippet = snippet,
                            reason = if (aligned != null) {
                                "AI-aligned streamer reaction to ${sc.authorName}"
                            } else {
                                "Donation at ${TimeUtils.formatTimestamp(sc.offsetSec)}"
                            }
                        )
                    )
                }
            }

            if (mode == DetectionMode.ALL || mode == DetectionMode.CHAT_HYPE) {
                allCandidates += chatScan.velocityClips
            }

            val hasNoSocialSignals = heatmap.isEmpty() && chatScan.superChats.isEmpty() && chatScan.velocityClips.isEmpty()
            if (mode == DetectionMode.AUDIO_PEAK || (mode == DetectionMode.ALL && hasNoSocialSignals)) {
                onProgress("Scanning audio/chapter highlights...")
                allCandidates += extractChapterOrTranscriptHighlights(infoJson, transcript, durationSec)
            }

            if ((mode == DetectionMode.ALL || mode == DetectionMode.AI_VIRAL) && !aiSettings.offlineMode) {
                onProgress("Running AI Viral Hook & Topic detection...")
                val anchors = allCandidates.map { (it.startSec + it.endSec) / 2.0 }
                allCandidates += aiClient.detectViralAndCustomClips(
                    settings = aiSettings,
                    videoTitle = title,
                    durationSec = durationSec,
                    transcript = transcript,
                    anchorTimestampsSec = anchors,
                    customQuery = customAiPrompt
                )
            }

            onProgress("Running Multi-Signal Consensus Engine...")
            val finalClips = ConsensusEngine.mergeAndRank(allCandidates)

            VideoAnalysisResult(
                sourceInput = url,
                isLocalFile = false,
                localFilePath = null,
                title = title,
                channelName = channel,
                durationSec = durationSec,
                heatmap = heatmap,
                clips = finalClips,
                transcriptCount = transcript.size,
                superChatCount = chatScan.superChats.size
            )
        }
    }

    suspend fun analyzeLocalVideo(
        uri: Uri,
        displayName: String,
        mode: DetectionMode,
        aiSettings: AiSettings,
        customAiPrompt: String,
        onProgress: (String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        runCatching {
            onProgress("Preparing local video file...")
            val cachedFile = File(
                context.cacheDir,
                "local_${System.currentTimeMillis()}_${TimeUtils.sanitizeFileName(displayName)}.mp4"
            )
            ffmpegRunner.copyUriToCache(uri, cachedFile).getOrThrow()

            val durationSec = ffmpegRunner.probeLocalDurationSec(cachedFile.absolutePath)

            onProgress("Scanning local audio waveform energy peaks...")
            val audioClips = ffmpegRunner.scanAudioEnergyPeaks(
                inputPath = cachedFile.absolutePath,
                durationSec = durationSec
            )

            val syntheticHeatmap = buildSyntheticEnergyCurve(audioClips, durationSec)

            val allCandidates = mutableListOf<ClipCandidate>()
            if (mode != DetectionMode.AI_VIRAL || aiSettings.offlineMode) {
                allCandidates += audioClips
            }

            if ((mode == DetectionMode.ALL || mode == DetectionMode.AI_VIRAL) &&
                !aiSettings.offlineMode &&
                customAiPrompt.isNotBlank()
            ) {
                onProgress("Refining clips with AI query...")
                val syntheticTranscript = audioClips.map {
                    TranscriptSegment(it.startSec, it.endSec, "${it.title}: ${it.reason}")
                }
                allCandidates += aiClient.detectViralAndCustomClips(
                    settings = aiSettings,
                    videoTitle = displayName,
                    durationSec = durationSec,
                    transcript = syntheticTranscript,
                    anchorTimestampsSec = audioClips.map { (it.startSec + it.endSec) / 2.0 },
                    customQuery = customAiPrompt
                )
            }

            val finalClips = ConsensusEngine.mergeAndRank(allCandidates)

            VideoAnalysisResult(
                sourceInput = displayName,
                isLocalFile = true,
                localFilePath = cachedFile.absolutePath,
                title = displayName.substringBeforeLast('.'),
                channelName = "Local Device Media",
                durationSec = durationSec,
                heatmap = syntheticHeatmap,
                clips = finalClips,
                transcriptCount = 0,
                superChatCount = 0
            )
        }
    }

    private fun parseHeatmap(infoJson: JSONObject): List<HeatmapPoint> {
        val arr = infoJson.optJSONArray("heatmap") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val obj = arr.optJSONObject(i) ?: continue
                val start = obj.optDouble("start_time", Double.NaN)
                val end = obj.optDouble("end_time", Double.NaN)
                val value = obj.optDouble("value", 0.0)
                if (!start.isNaN() && !end.isNaN()) {
                    add(HeatmapPoint(start, end, value.coerceIn(0.0, 1.0)))
                }
            }
        }
    }

    private fun extractHeatmapClips(
        heatmap: List<HeatmapPoint>,
        transcript: List<TranscriptSegment>,
        durationSec: Double
    ): List<ClipCandidate> {
        if (heatmap.size < 3) return emptyList()

        val peaks = mutableListOf<HeatmapPoint>()
        for (i in 1 until heatmap.size - 1) {
            val prev = heatmap[i - 1].value
            val curr = heatmap[i].value
            val next = heatmap[i + 1].value
            if (curr >= prev && curr >= next && curr >= 0.45) {
                peaks.add(heatmap[i])
            }
        }

        val topPeaks = peaks.sortedByDescending { it.value }.take(10)
        val result = mutableListOf<ClipCandidate>()
        for (peak in topPeaks) {
            val center = (peak.startSec + peak.endSec) / 2.0
            if (result.any { kotlin.math.abs(((it.startSec + it.endSec) / 2.0) - center) < 20.0 }) {
                continue
            }
            val start = (center - 14.0).coerceAtLeast(0.0)
            val end = (center + 18.0).coerceAtMost(durationSec)
            val score = (68 + (peak.value * 32.0)).toInt().coerceIn(65, 100)
            val snippet = transcript.filter { it.endSec >= start && it.startSec <= end }
                .joinToString(" ") { it.text }
                .take(240)

            result.add(
                ClipCandidate(
                    title = "Most Replayed Peak (${(peak.value * 100).toInt()}%)",
                    startSec = start,
                    endSec = end,
                    score = score,
                    signals = listOf(SignalType.HEATMAP),
                    transcriptSnippet = snippet,
                    reason = String.format(
                        Locale.US,
                        "Viewer replay intensity %.0f%% at %s",
                        peak.value * 100.0,
                        TimeUtils.formatTimestamp(center)
                    )
                )
            )
        }
        return result.sortedBy { it.startSec }
    }

    private fun extractChapterOrTranscriptHighlights(
        infoJson: JSONObject,
        transcript: List<TranscriptSegment>,
        durationSec: Double
    ): List<ClipCandidate> {
        val chapters = infoJson.optJSONArray("chapters")
        if (chapters != null && chapters.length() > 0) {
            return buildList {
                for (i in 0 until minOf(chapters.length(), 8)) {
                    val ch = chapters.optJSONObject(i) ?: continue
                    val start = ch.optDouble("start_time", 0.0)
                    val end = ch.optDouble("end_time", (start + 30.0).coerceAtMost(durationSec))
                    val chTitle = ch.optString("title").ifBlank { "Chapter #${i + 1}" }
                    add(
                        ClipCandidate(
                            title = chTitle,
                            startSec = start,
                            endSec = end.coerceAtMost(start + 60.0),
                            score = 78,
                            signals = listOf(SignalType.AUDIO_PEAK),
                            reason = "Video chapter highlight"
                        )
                    )
                }
            }
        }

        if (transcript.isNotEmpty()) {
            val excitementWords = listOf("!", "?", "what", "no way", "crazy", "insane", "bro", "omg", "haha", "let's go")
            val scoredSegs = transcript.map { seg ->
                val lower = seg.text.lowercase(Locale.US)
                val hits = excitementWords.count { lower.contains(it) }
                Pair(seg, hits)
            }.filter { it.second > 0 }.sortedByDescending { it.second }

            val clips = mutableListOf<ClipCandidate>()
            for ((seg, hits) in scoredSegs) {
                if (clips.size >= 6) break
                if (clips.any { kotlin.math.abs(it.startSec - seg.startSec) < 25.0 }) continue
                val start = (seg.startSec - 10.0).coerceAtLeast(0.0)
                val end = (seg.endSec + 20.0).coerceAtMost(durationSec)
                clips.add(
                    ClipCandidate(
                        title = "Highlight @ ${TimeUtils.formatTimestamp(seg.startSec)}",
                        startSec = start,
                        endSec = end,
                        score = (72 + hits * 6).coerceIn(72, 92),
                        signals = listOf(SignalType.AUDIO_PEAK),
                        transcriptSnippet = seg.text.take(240),
                        reason = "High-energy dialogue cue"
                    )
                )
            }
            if (clips.isNotEmpty()) return clips.sortedBy { it.startSec }
        }

        val count = (durationSec / 60.0).toInt().coerceIn(2, 5)
        val step = durationSec / (count + 1)
        return (1..count).map { idx ->
            val center = idx * step
            ClipCandidate(
                title = "Highlight Window #$idx",
                startSec = (center - 15.0).coerceAtLeast(0.0),
                endSec = (center + 15.0).coerceAtMost(durationSec),
                score = 70,
                signals = listOf(SignalType.AUDIO_PEAK),
                reason = "Auto-segmented highlight candidate"
            )
        }
    }

    private fun buildSyntheticEnergyCurve(
        clips: List<ClipCandidate>,
        durationSec: Double
    ): List<HeatmapPoint> {
        val bins = 40
        val binWidth = (durationSec / bins).coerceAtLeast(1.0)
        return (0 until bins).map { idx ->
            val bStart = idx * binWidth
            val bEnd = (idx + 1) * binWidth
            val bMid = (bStart + bEnd) / 2.0
            val matchingClip = clips.firstOrNull { bMid in it.startSec..it.endSec }
            val value = if (matchingClip != null) {
                (matchingClip.score / 100.0).coerceIn(0.4, 1.0)
            } else {
                0.18 + (idx % 4) * 0.04
            }
            HeatmapPoint(bStart, bEnd, value)
        }
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/engine/ClipExporter.kt"] = r'''package com.clippulse.studio.engine

import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.clippulse.studio.ClipPulseApp
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.ExportConfig
import com.clippulse.studio.model.VideoAnalysisResult
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.util.Locale

class ClipExporter(
    private val context: Context,
    private val ffmpegRunner: FfmpegRunner
) {

    suspend fun exportSingleClip(
        analysis: VideoAnalysisResult,
        clip: ClipCandidate,
        config: ExportConfig,
        onStatus: (String) -> Unit
    ): Result<String> = withContext(Dispatchers.IO) {
        runCatching {
            ClipPulseApp.ensureEnginesInitialized(context).getOrThrow()

            val paddedStart = (clip.startSec - config.startPaddingSec).coerceAtLeast(0.0)
            val paddedEnd = (clip.endSec + config.endPaddingSec)
                .coerceAtMost(analysis.durationSec)
                .coerceAtLeast(paddedStart + 2.0)

            val tempDir = File(context.cacheDir, "export_tmp").apply { mkdirs() }
            val safeBase = "${TimeUtils.sanitizeFileName(clip.title)}_${System.currentTimeMillis()}"
            val rawSectionFile = File(tempDir, "${safeBase}_raw.mp4")
            val finalOutputFile = File(tempDir, "${safeBase}_final.mp4")

            if (analysis.isLocalFile && !analysis.localFilePath.isNullOrBlank()) {
                onStatus("Slicing local video section...")
                val duration = (paddedEnd - paddedStart).coerceAtLeast(1.0)
                val ffmpegArgs = if (config.useVerticalCrop) {
                    listOf(
                        "-y",
                        "-ss", String.format(Locale.US, "%.2f", paddedStart),
                        "-i", analysis.localFilePath,
                        "-t", String.format(Locale.US, "%.2f", duration),
                        "-vf", "crop=ih*9/16:ih",
                        "-c:v", "libx264",
                        "-preset", "fast",
                        "-crf", "21",
                        "-c:a", "aac",
                        "-b:a", "128k",
                        finalOutputFile.absolutePath
                    )
                } else {
                    listOf(
                        "-y",
                        "-ss", String.format(Locale.US, "%.2f", paddedStart),
                        "-i", analysis.localFilePath,
                        "-t", String.format(Locale.US, "%.2f", duration),
                        "-c", "copy",
                        finalOutputFile.absolutePath
                    )
                }
                val ffRes = ffmpegRunner.execute(ffmpegArgs)
                if (ffRes.exitCode != 0 || !finalOutputFile.exists()) {
                    error("FFmpeg local slice failed: ${ffRes.output.takeLast(180)}")
                }
            } else {
                val sectionArg = TimeUtils.formatDownloadSection(paddedStart, paddedEnd)
                onStatus("Downloading section $sectionArg (up to 1080p)...")

                val request = YoutubeDLRequest(analysis.sourceInput).apply {
                    addOption(
                        "-f",
                        "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]"
                    )
                    addOption("--download-sections", sectionArg)
                    addOption("--force-keyframes-at-cuts")
                    addOption("--merge-output-format", "mp4")
                    addOption("--no-playlist")
                    addOption("-o", rawSectionFile.absolutePath)
                }

                val dlRes = YoutubeDL.getInstance().execute(request) { progress, _, _ ->
                    if (progress >= 0f) {
                        onStatus("Downloading section $sectionArg (${progress.toInt()}%)...")
                    }
                }

                val downloadedFile = tempDir.listFiles()?.firstOrNull {
                    it.name.startsWith("${safeBase}_raw") && it.length() > 0L
                } ?: error("Section download failed: ${dlRes.err.takeLast(180)}")

                if (config.useVerticalCrop) {
                    onStatus("Applying 9:16 vertical crop...")
                    val cropRes = ffmpegRunner.execute(
                        listOf(
                            "-y",
                            "-i", downloadedFile.absolutePath,
                            "-vf", "crop=ih*9/16:ih",
                            "-c:v", "libx264",
                            "-preset", "fast",
                            "-crf", "21",
                            "-c:a", "aac",
                            "-b:a", "128k",
                            finalOutputFile.absolutePath
                        )
                    )
                    if (cropRes.exitCode != 0 || !finalOutputFile.exists()) {
                        error("9:16 vertical crop failed: ${cropRes.output.takeLast(180)}")
                    }
                } else {
                    downloadedFile.copyTo(finalOutputFile, overwrite = true)
                }
            }

            onStatus("Saving to Gallery (/Movies/ClipPulse)...")
            val displayFilename = "${TimeUtils.sanitizeFileName(clip.title)}_${TimeUtils.formatTimestamp(paddedStart).replace(':', '-')}.mp4"
            saveVideoToGallery(finalOutputFile, displayFilename)

            if (config.includeTxtSidecar) {
                saveTxtSidecar(
                    analysis = analysis,
                    clip = clip,
                    paddedStart = paddedStart,
                    paddedEnd = paddedEnd,
                    baseFilename = displayFilename.removeSuffix(".mp4")
                )
            }

            rawSectionFile.delete()
            finalOutputFile.delete()
            displayFilename
        }
    }

    private fun saveVideoToGallery(sourceFile: File, displayName: String) {
        val resolver = context.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.Video.Media.DISPLAY_NAME, displayName)
            put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                put(
                    MediaStore.Video.Media.RELATIVE_PATH,
                    "${Environment.DIRECTORY_MOVIES}/ClipPulse"
                )
                put(MediaStore.Video.Media.IS_PENDING, 1)
            }
        }

        val itemUri = resolver.insert(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, values)
            ?: error("MediaStore failed to create Gallery entry")

        resolver.openOutputStream(itemUri)?.use { out ->
            sourceFile.inputStream().use { input ->
                input.copyTo(out, bufferSize = 65536)
            }
        } ?: error("Unable to write video stream to Gallery")

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val complete = ContentValues().apply {
                put(MediaStore.Video.Media.IS_PENDING, 0)
            }
            resolver.update(itemUri, complete, null, null)
        }
    }

    private fun saveTxtSidecar(
        analysis: VideoAnalysisResult,
        clip: ClipCandidate,
        paddedStart: Double,
        paddedEnd: Double,
        baseFilename: String
    ) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) return
        val sidecarText = buildString {
            appendLine("ClipPulse Studio Export Note")
            appendLine("============================")
            appendLine("Clip Title: ${clip.title}")
            appendLine("Source Title: ${analysis.title}")
            appendLine("Source URL: ${analysis.sourceInput}")
            appendLine("Range: ${TimeUtils.formatTimestamp(paddedStart)} - ${TimeUtils.formatTimestamp(paddedEnd)}")
            appendLine("Hype Score: ${clip.score}/100")
            appendLine("Signals: ${clip.signals.joinToString(", ") { it.label }}")
            if (clip.superChat != null) {
                appendLine("Super Chat: ${clip.superChat.amountText} from ${clip.superChat.authorName}")
                if (clip.superChat.message.isNotBlank()) {
                    appendLine("Donor Message: ${clip.superChat.message}")
                }
            }
            if (clip.reason.isNotBlank()) {
                appendLine("Detection Note: ${clip.reason}")
            }
            if (clip.transcriptSnippet.isNotBlank()) {
                appendLine()
                appendLine("Transcript Snippet:")
                appendLine(clip.transcriptSnippet)
            }
        }

        val resolver = context.contentResolver
        val values = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, "$baseFilename.txt")
            put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
            put(
                MediaStore.MediaColumns.RELATIVE_PATH,
                "${Environment.DIRECTORY_DOCUMENTS}/ClipPulse"
            )
        }
        runCatching {
            val uri = resolver.insert(MediaStore.Files.getContentUri("external"), values) ?: return
            resolver.openOutputStream(uri)?.use { out ->
                out.write(sidecarText.toByteArray(Charsets.UTF_8))
            }
        }
    }
}
'''

# ==============================================================================
# 7. FOREGROUND SERVICE (DATA SYNC)
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/service/ClipExportService.kt"] = r'''package com.clippulse.studio.service

import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.clippulse.studio.ClipPulseApp
import com.clippulse.studio.MainActivity
import com.clippulse.studio.engine.ClipExporter
import com.clippulse.studio.engine.FfmpegRunner
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.ExportConfig
import com.clippulse.studio.model.ExportProgressState
import com.clippulse.studio.model.VideoAnalysisResult
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

object ExportSessionHolder {
    var pendingAnalysis: VideoAnalysisResult? = null
    var pendingClips: List<ClipCandidate> = emptyList()
    var pendingConfig: ExportConfig = ExportConfig()

    private val _progress = MutableStateFlow(ExportProgressState())
    val progress: StateFlow<ExportProgressState> = _progress.asStateFlow()

    fun update(state: ExportProgressState) {
        _progress.value = state
    }
}

class ClipExportService : Service() {

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var exportJob: Job? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val analysis = ExportSessionHolder.pendingAnalysis
        val clips = ExportSessionHolder.pendingClips
        val config = ExportSessionHolder.pendingConfig

        if (analysis == null || clips.isEmpty()) {
            stopSelf()
            return START_NOT_STICKY
        }

        val notification = buildNotification(
            title = "Exporting ${clips.size} clip(s) to Gallery",
            text = "Preparing section-only pipeline...",
            progress = 0,
            max = 100
        )

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(
                NOTIFICATION_ID,
                notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
            )
        } else {
            startForeground(NOTIFICATION_ID, notification)
        }

        exportJob?.cancel()
        exportJob = serviceScope.launch {
            val exporter = ClipExporter(applicationContext, FfmpegRunner(applicationContext))
            val completed = mutableListOf<String>()
            var lastError: String? = null

            clips.forEachIndexed { idx, clip ->
                val baseFraction = idx.toFloat() / clips.size.toFloat()
                ExportSessionHolder.update(
                    ExportProgressState(
                        isExporting = true,
                        currentIndex = idx + 1,
                        totalCount = clips.size,
                        currentTitle = clip.title,
                        fraction = baseFraction,
                        statusMessage = "Clip ${idx + 1}/${clips.size}: ${clip.title}",
                        completedTitles = completed.toList()
                    )
                )
                updateNotification(
                    title = "Exporting Clip ${idx + 1} of ${clips.size}",
                    text = clip.title,
                    progress = (baseFraction * 100).toInt(),
                    max = 100
                )

                val res = exporter.exportSingleClip(
                    analysis = analysis,
                    clip = clip,
                    config = config
                ) { stepText ->
                    ExportSessionHolder.update(
                        ExportProgressState(
                            isExporting = true,
                            currentIndex = idx + 1,
                            totalCount = clips.size,
                            currentTitle = clip.title,
                            fraction = baseFraction + (0.5f / clips.size.toFloat()),
                            statusMessage = stepText,
                            completedTitles = completed.toList()
                        )
                    )
                }

                res.onSuccess { savedName ->
                    completed.add(savedName)
                }.onFailure { err ->
                    lastError = err.message ?: "Export error"
                }
            }

            val finalMsg = if (completed.isNotEmpty()) {
                "Saved ${completed.size}/${clips.size} clip(s) to /Movies/ClipPulse"
            } else {
                lastError ?: "Export failed"
            }

            ExportSessionHolder.update(
                ExportProgressState(
                    isExporting = false,
                    currentIndex = clips.size,
                    totalCount = clips.size,
                    currentTitle = "",
                    fraction = 1f,
                    statusMessage = finalMsg,
                    completedTitles = completed,
                    errorMessage = if (completed.isEmpty()) lastError else null
                )
            )

            updateNotification(
                title = "ClipPulse Export Complete",
                text = finalMsg,
                progress = 100,
                max = 100
            )
            stopForeground(STOP_FOREGROUND_DETACH)
            stopSelf()
        }

        return START_NOT_STICKY
    }

    private fun updateNotification(title: String, text: String, progress: Int, max: Int) {
        val manager = getSystemService(NotificationManager::class.java)
        manager?.notify(NOTIFICATION_ID, buildNotification(title, text, progress, max))
    }

    private fun buildNotification(title: String, text: String, progress: Int, max: Int) =
        NotificationCompat.Builder(this, ClipPulseApp.EXPORT_CHANNEL_ID)
            .setSmallIcon(android.R.drawable.stat_sys_download)
            .setContentTitle(title)
            .setContentText(text)
            .setOnlyAlertOnce(true)
            .setOngoing(progress < max)
            .setProgress(max, progress, progress == 0)
            .setContentIntent(
                PendingIntent.getActivity(
                    this,
                    0,
                    Intent(this, MainActivity::class.java),
                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
                )
            )
            .build()

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    companion object {
        private const val NOTIFICATION_ID = 4091

        fun startExport(
            context: Context,
            analysis: VideoAnalysisResult,
            selectedClips: List<ClipCandidate>,
            config: ExportConfig
        ) {
            ExportSessionHolder.pendingAnalysis = analysis
            ExportSessionHolder.pendingClips = selectedClips
            ExportSessionHolder.pendingConfig = config

            val intent = Intent(context, ClipExportService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }
    }
}
'''

# ==============================================================================
# 8. VIEWMODEL & JETPACK COMPOSE DARK-MODE STUDIO UI
# ==============================================================================

FILES["app/src/main/java/com/clippulse/studio/ui/theme/Theme.kt"] = r'''package com.clippulse.studio.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val ObsidianBg = Color(0xFF0B0B0F)
val MatteSlateCard = Color(0xFF16161D)
val ElevatedSlate = Color(0xFF1F1F29)
val HairlineBorder = Color(0xFF262633)
val ElectricIndigo = Color(0xFF6366F1)
val ElectricIndigoDark = Color(0xFF4F46E5)

val SuperChatGold = Color(0xFFF59E0B)
val HeatmapCrimson = Color(0xFFEF4444)
val ChatHypePurple = Color(0xFFA855F7)
val AiPickCyan = Color(0xFF06B6D4)
val MultiSignalOrange = Color(0xFFFB923C)
val SuccessGreen = Color(0xFF10B981)

val TextPrimary = Color(0xFFF4F4F6)
val TextSecondary = Color(0xFFA1A1B5)
val TextMuted = Color(0xFF6E6E85)

private val ClipPulseColorScheme = darkColorScheme(
    primary = ElectricIndigo,
    onPrimary = Color.White,
    primaryContainer = ElectricIndigoDark,
    onPrimaryContainer = Color.White,
    secondary = AiPickCyan,
    onSecondary = ObsidianBg,
    background = ObsidianBg,
    onBackground = TextPrimary,
    surface = MatteSlateCard,
    onSurface = TextPrimary,
    surfaceVariant = ElevatedSlate,
    onSurfaceVariant = TextSecondary,
    outline = HairlineBorder,
    outlineVariant = HairlineBorder,
    error = HeatmapCrimson,
    onError = Color.White
)

@Composable
fun ClipPulseTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = ClipPulseColorScheme,
        content = content
    )
}
'''

FILES["app/src/main/java/com/clippulse/studio/ui/ClipPulseViewModel.kt"] = r'''package com.clippulse.studio.ui

import android.app.Application
import android.net.Uri
import android.provider.OpenableColumns
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.clippulse.studio.ClipPulseApp
import com.clippulse.studio.data.AiConfigRepository
import com.clippulse.studio.engine.FfmpegRunner
import com.clippulse.studio.engine.VideoAnalysisEngine
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.AiProviderPreset
import com.clippulse.studio.model.AiSettings
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.ExportConfig
import com.clippulse.studio.model.ExportProgressState
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.model.VideoAnalysisResult
import com.clippulse.studio.network.UniversalAiClient
import com.clippulse.studio.service.ClipExportService
import com.clippulse.studio.service.ExportSessionHolder
import com.yausername.youtubedl_android.YoutubeDL
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

enum class SignalFilter(val label: String) {
    ALL("All"),
    MULTI("Multi-Signal"),
    SUPER_CHAT("Super Chat"),
    HEATMAP("Heatmap"),
    CHAT_HYPE("Chat Hype"),
    AI_PICK("AI Pick")
}

data class StudioUiState(
    val urlInput: String = "",
    val selectedLocalUri: Uri? = null,
    val selectedLocalName: String = "",
    val detectionMode: DetectionMode = DetectionMode.ALL,
    val customAiQuery: String = "",
    val minSuperChatUsd: Double = 0.0,
    val isAnalyzing: Boolean = false,
    val analysisStepText: String = "",
    val analysisError: String? = null,
    val analysisResult: VideoAnalysisResult? = null,
    val activeFilter: SignalFilter = SignalFilter.ALL,
    val focusedClipId: String? = null,
    val aiSettings: AiSettings = AiSettings(),
    val aiConnectionState: AiConnectionState = AiConnectionState.Disconnected,
    val isFetchingModels: Boolean = false,
    val modelFetchMessage: String? = null,
    val isUpdatingYtDlp: Boolean = false,
    val ytDlpUpdateMessage: String? = null,
    val showAiManagerSheet: Boolean = false,
    val exportConfig: ExportConfig = ExportConfig()
)

class ClipPulseViewModel(application: Application) : AndroidViewModel(application) {

    private val configRepo = AiConfigRepository(application)
    private val aiClient = UniversalAiClient()
    private val ffmpegRunner = FfmpegRunner(application)
    private val analysisEngine = VideoAnalysisEngine(application, aiClient, ffmpegRunner)

    private val _uiState = MutableStateFlow(
        StudioUiState(
            aiSettings = configRepo.loadAiSettings(),
            exportConfig = configRepo.loadExportConfig()
        )
    )
    val uiState: StateFlow<StudioUiState> = _uiState.asStateFlow()

    val exportProgress: StateFlow<ExportProgressState> = ExportSessionHolder.progress

    fun onUrlChanged(newUrl: String) {
        _uiState.update {
            it.copy(
                urlInput = newUrl,
                selectedLocalUri = null,
                selectedLocalName = "",
                analysisError = null
            )
        }
    }

    fun onLocalVideoSelected(uri: Uri) {
        val name = resolveFileName(uri)
        _uiState.update {
            it.copy(
                selectedLocalUri = uri,
                selectedLocalName = name,
                urlInput = "",
                analysisError = null
            )
        }
    }

    fun onDetectionModeSelected(mode: DetectionMode) {
        _uiState.update { it.copy(detectionMode = mode) }
    }

    fun onCustomAiQueryChanged(query: String) {
        _uiState.update { it.copy(customAiQuery = query) }
    }

    fun onMinSuperChatChanged(minAmount: Double) {
        _uiState.update { it.copy(minSuperChatUsd = minAmount) }
    }

    fun onSignalFilterSelected(filter: SignalFilter) {
        _uiState.update { it.copy(activeFilter = filter) }
    }

    fun onFocusClip(clipId: String?) {
        _uiState.update { it.copy(focusedClipId = clipId) }
    }

    fun toggleAiManagerSheet(show: Boolean) {
        _uiState.update { it.copy(showAiManagerSheet = show) }
    }

    fun selectAiPreset(preset: AiProviderPreset) {
        val updated = _uiState.value.aiSettings.copy(
            preset = preset,
            baseUrl = preset.defaultBaseUrl,
            selectedModel = preset.defaultModel
        )
        configRepo.saveAiSettings(updated)
        _uiState.update {
            it.copy(
                aiSettings = updated,
                aiConnectionState = AiConnectionState.Disconnected,
                modelFetchMessage = null
            )
        }
    }

    fun updateAiSettings(transform: (AiSettings) -> AiSettings) {
        val updated = transform(_uiState.value.aiSettings)
        configRepo.saveAiSettings(updated)
        _uiState.update { it.copy(aiSettings = updated) }
    }

    fun addBackupKey(newKey: String) {
        val trimmed = newKey.trim()
        if (trimmed.isEmpty()) return
        updateAiSettings { current ->
            if (current.backupApiKeys.contains(trimmed)) current
            else current.copy(backupApiKeys = current.backupApiKeys + trimmed)
        }
    }

    fun removeBackupKey(keyToRemove: String) {
        updateAiSettings { current ->
            current.copy(backupApiKeys = current.backupApiKeys.filterNot { it == keyToRemove })
        }
    }

    fun fetchModels() {
        viewModelScope.launch {
            _uiState.update { it.copy(isFetchingModels = true, modelFetchMessage = null) }
            val currentSettings = _uiState.value.aiSettings
            val res = aiClient.fetchModels(currentSettings)
            res.onSuccess { models ->
                val chosenModel = if (models.contains(currentSettings.selectedModel)) {
                    currentSettings.selectedModel
                } else {
                    models.first()
                }
                val updated = currentSettings.copy(
                    availableModels = models,
                    selectedModel = chosenModel
                )
                configRepo.saveAiSettings(updated)
                _uiState.update {
                    it.copy(
                        isFetchingModels = false,
                        aiSettings = updated,
                        modelFetchMessage = "Loaded ${models.size} models"
                    )
                }
            }.onFailure { err ->
                _uiState.update {
                    it.copy(
                        isFetchingModels = false,
                        modelFetchMessage = err.message ?: "Failed to fetch models"
                    )
                }
            }
        }
    }

    fun connectAiModel() {
        viewModelScope.launch {
            _uiState.update { it.copy(aiConnectionState = AiConnectionState.Testing) }
            val settings = _uiState.value.aiSettings
            val res = aiClient.testConnection(settings)
            res.onSuccess { latencyMs ->
                _uiState.update {
                    it.copy(
                        aiConnectionState = AiConnectionState.Connected(
                            latencyMs = latencyMs,
                            model = settings.selectedModel
                        )
                    )
                }
            }.onFailure { err ->
                _uiState.update {
                    it.copy(
                        aiConnectionState = AiConnectionState.Error(
                            err.message ?: "Connection failed"
                        )
                    )
                }
            }
        }
    }

    fun updateYtDlpEngine() {
        viewModelScope.launch {
            _uiState.update {
                it.copy(isUpdatingYtDlp = true, ytDlpUpdateMessage = "Updating yt-dlp binary...")
            }
            val msg = withContext(Dispatchers.IO) {
                ClipPulseApp.ensureEnginesInitialized(getApplication())
                runCatching {
                    val status = YoutubeDL.getInstance().updateYoutubeDL(getApplication())
                    "yt-dlp status: ${status?.name ?: "UP TO DATE"}"
                }.getOrElse { err ->
                    "Update failed: ${err.message ?: "Network error"}"
                }
            }
            _uiState.update {
                it.copy(isUpdatingYtDlp = false, ytDlpUpdateMessage = msg)
            }
        }
    }

    fun startAnalysis() {
        val state = _uiState.value
        if (state.isAnalyzing) return

        val localUri = state.selectedLocalUri
        val rawUrl = state.urlInput.trim()

        if (localUri == null && rawUrl.isBlank()) {
            _uiState.update { it.copy(analysisError = "Paste a YouTube/Facebook URL or pick a local video first.") }
            return
        }

        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    isAnalyzing = true,
                    analysisError = null,
                    analysisStepText = "Starting zero-download metadata scan...",
                    activeFilter = SignalFilter.ALL
                )
            }

            val result = if (localUri != null) {
                analysisEngine.analyzeLocalVideo(
                    uri = localUri,
                    displayName = state.selectedLocalName.ifBlank { "Local_Video.mp4" },
                    mode = state.detectionMode,
                    aiSettings = state.aiSettings,
                    customAiPrompt = state.customAiQuery.trim()
                ) { step ->
                    _uiState.update { it.copy(analysisStepText = step) }
                }
            } else {
                analysisEngine.analyzeRemoteUrl(
                    url = rawUrl,
                    mode = state.detectionMode,
                    aiSettings = state.aiSettings,
                    minSuperChatUsd = state.minSuperChatUsd,
                    customAiPrompt = state.customAiQuery.trim()
                ) { step ->
                    _uiState.update { it.copy(analysisStepText = step) }
                }
            }

            result.onSuccess { analysis ->
                _uiState.update {
                    it.copy(
                        isAnalyzing = false,
                        analysisResult = analysis,
                        analysisStepText = "",
                        focusedClipId = analysis.clips.firstOrNull()?.id
                    )
                }
            }.onFailure { err ->
                _uiState.update {
                    it.copy(
                        isAnalyzing = false,
                        analysisStepText = "",
                        analysisError = err.message ?: "Analysis failed"
                    )
                }
            }
        }
    }

    fun toggleClipSelection(clipId: String) {
        val analysis = _uiState.value.analysisResult ?: return
        val updatedClips = analysis.clips.map { clip ->
            if (clip.id == clipId) clip.copy(selected = !clip.selected) else clip
        }
        _uiState.update {
            it.copy(analysisResult = analysis.copy(clips = updatedClips))
        }
    }

    fun selectAllVisibleClips(select: Boolean) {
        val analysis = _uiState.value.analysisResult ?: return
        val filter = _uiState.value.activeFilter
        val updatedClips = analysis.clips.map { clip ->
            if (matchesFilter(clip, filter)) clip.copy(selected = select) else clip
        }
        _uiState.update {
            it.copy(analysisResult = analysis.copy(clips = updatedClips))
        }
    }

    fun nudgeClipStart(clipId: String, deltaSec: Double) {
        val analysis = _uiState.value.analysisResult ?: return
        val updatedClips = analysis.clips.map { clip ->
            if (clip.id == clipId) {
                val newStart = (clip.startSec + deltaSec)
                    .coerceIn(0.0, (clip.endSec - 2.0).coerceAtLeast(0.0))
                clip.copy(startSec = newStart)
            } else clip
        }
        _uiState.update {
            it.copy(analysisResult = analysis.copy(clips = updatedClips))
        }
    }

    fun nudgeClipEnd(clipId: String, deltaSec: Double) {
        val analysis = _uiState.value.analysisResult ?: return
        val updatedClips = analysis.clips.map { clip ->
            if (clip.id == clipId) {
                val newEnd = (clip.endSec + deltaSec)
                    .coerceIn(clip.startSec + 2.0, analysis.durationSec)
                clip.copy(endSec = newEnd)
            } else clip
        }
        _uiState.update {
            it.copy(analysisResult = analysis.copy(clips = updatedClips))
        }
    }

    fun updateExportConfig(transform: (ExportConfig) -> ExportConfig) {
        val updated = transform(_uiState.value.exportConfig)
        configRepo.saveExportConfig(updated)
        _uiState.update { it.copy(exportConfig = updated) }
    }

    fun exportSelectedClips() {
        val analysis = _uiState.value.analysisResult ?: return
        val selected = analysis.clips.filter { it.selected }
        if (selected.isEmpty()) return

        ClipExportService.startExport(
            context = getApplication(),
            analysis = analysis,
            selectedClips = selected,
            config = _uiState.value.exportConfig
        )
    }

    fun matchesFilter(clip: ClipCandidate, filter: SignalFilter): Boolean {
        return when (filter) {
            SignalFilter.ALL -> true
            SignalFilter.MULTI -> clip.isMultiSignal
            SignalFilter.SUPER_CHAT -> clip.signals.contains(SignalType.SUPER_CHAT)
            SignalFilter.HEATMAP -> clip.signals.contains(SignalType.HEATMAP)
            SignalFilter.CHAT_HYPE -> clip.signals.contains(SignalType.CHAT_HYPE)
            SignalFilter.AI_PICK -> clip.signals.contains(SignalType.AI_PICK)
        }
    }

    private fun resolveFileName(uri: Uri): String {
        val resolver = getApplication<Application>().contentResolver
        resolver.query(uri, null, null, null, null)?.use { cursor ->
            val idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
            if (idx >= 0 && cursor.moveToFirst()) {
                return cursor.getString(idx) ?: "Local_Video.mp4"
            }
        }
        return uri.lastPathSegment?.substringAfterLast('/') ?: "Local_Video.mp4"
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/ui/components/HeatmapTimeline.kt"] = r'''package com.clippulse.studio.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.engine.TimeUtils
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.HeatmapPoint
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.ui.theme.AiPickCyan
import com.clippulse.studio.ui.theme.ChatHypePurple
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.HeatmapCrimson
import com.clippulse.studio.ui.theme.SuperChatGold
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextSecondary
import kotlin.math.abs

@Composable
fun HeatmapTimeline(
    durationSec: Double,
    heatmap: List<HeatmapPoint>,
    clips: List<ClipCandidate>,
    focusedClipId: String?,
    onSelectClipFromTimeline: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val safeDuration = durationSec.coerceAtLeast(1.0)

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "SIGNAL TIMELINE & REPLAY CURVE",
                color = TextSecondary,
                fontSize = 11.sp,
                fontWeight = FontWeight.SemiBold
            )
            Text(
                text = "${clips.size} candidate(s)",
                color = AiPickCyan,
                fontSize = 11.sp,
                fontWeight = FontWeight.Medium
            )
        }

        Spacer(modifier = Modifier.height(8.dp))

        Canvas(
            modifier = Modifier
                .fillMaxWidth()
                .height(84.dp)
                .pointerInput(clips, safeDuration) {
                    detectTapGestures { offset ->
                        if (clips.isEmpty() || size.width <= 0) return@detectTapGestures
                        val tappedSec = (offset.x / size.width.toFloat()) * safeDuration
                        val nearest = clips.minByOrNull { clip ->
                            val mid = (clip.startSec + clip.endSec) / 2.0
                            abs(mid - tappedSec)
                        }
                        if (nearest != null) {
                            onSelectClipFromTimeline(nearest.id)
                        }
                    }
                }
        ) {
            val w = size.width
            val h = size.height
            val bottomY = h - 4.dp.toPx()
            val topPad = 8.dp.toPx()
            val chartHeight = (bottomY - topPad).coerceAtLeast(10f)

            drawLine(
                color = HairlineBorder,
                start = Offset(0f, bottomY),
                end = Offset(w, bottomY),
                strokeWidth = 1.dp.toPx()
            )
            drawLine(
                color = HairlineBorder.copy(alpha = 0.45f),
                start = Offset(0f, topPad + chartHeight * 0.5f),
                end = Offset(w, topPad + chartHeight * 0.5f),
                strokeWidth = 1.dp.toPx()
            )

            if (heatmap.size >= 2) {
                val strokePath = Path()
                val fillPath = Path()

                heatmap.forEachIndexed { idx, pt ->
                    val midSec = ((pt.startSec + pt.endSec) / 2.0).coerceIn(0.0, safeDuration)
                    val x = ((midSec / safeDuration) * w).toFloat()
                    val y = bottomY - (pt.value.toFloat().coerceIn(0f, 1f) * chartHeight)

                    if (idx == 0) {
                        strokePath.moveTo(x, y)
                        fillPath.moveTo(x, bottomY)
                        fillPath.lineTo(x, y)
                    } else {
                        strokePath.lineTo(x, y)
                        fillPath.lineTo(x, y)
                    }
                    if (idx == heatmap.lastIndex) {
                        fillPath.lineTo(x, bottomY)
                        fillPath.close()
                    }
                }

                drawPath(
                    path = fillPath,
                    brush = Brush.verticalGradient(
                        colors = listOf(
                            HeatmapCrimson.copy(alpha = 0.35f),
                            ElectricIndigo.copy(alpha = 0.05f)
                        )
                    )
                )
                drawPath(
                    path = strokePath,
                    color = HeatmapCrimson.copy(alpha = 0.85f),
                    style = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round)
                )
            }

            for (clip in clips) {
                val startX = ((clip.startSec / safeDuration) * w).toFloat().coerceIn(0f, w)
                val endX = ((clip.endSec / safeDuration) * w).toFloat().coerceIn(startX + 2f, w)
                val markerColor = primarySignalColor(clip)
                val isFocused = clip.id == focusedClipId

                drawRect(
                    color = markerColor.copy(alpha = if (isFocused) 0.34f else if (clip.selected) 0.18f else 0.07f),
                    topLeft = Offset(startX, topPad),
                    size = Size((endX - startX).coerceAtLeast(3f), chartHeight)
                )

                val centerX = (startX + endX) / 2f
                drawLine(
                    color = markerColor.copy(alpha = if (clip.selected) 0.95f else 0.45f),
                    start = Offset(centerX, 2.dp.toPx()),
                    end = Offset(centerX, bottomY),
                    strokeWidth = if (isFocused) 3.dp.toPx() else 2.dp.toPx(),
                    cap = StrokeCap.Round
                )
            }
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 4.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("00:00", color = TextMuted, fontSize = 10.sp)
            Text(TimeUtils.formatTimestamp(safeDuration / 2.0), color = TextMuted, fontSize = 10.sp)
            Text(TimeUtils.formatTimestamp(safeDuration), color = TextMuted, fontSize = 10.sp)
        }
    }
}

fun primarySignalColor(clip: ClipCandidate): Color {
    return when {
        clip.signals.contains(SignalType.SUPER_CHAT) -> SuperChatGold
        clip.signals.contains(SignalType.HEATMAP) -> HeatmapCrimson
        clip.signals.contains(SignalType.CHAT_HYPE) -> ChatHypePurple
        clip.signals.contains(SignalType.AI_PICK) -> AiPickCyan
        else -> ElectricIndigo
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/ui/components/ClipCard.kt"] = r'''@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)

package com.clippulse.studio.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.MonetizationOn
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.engine.TimeUtils
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalType
import com.clippulse.studio.ui.theme.AiPickCyan
import com.clippulse.studio.ui.theme.ChatHypePurple
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.HeatmapCrimson
import com.clippulse.studio.ui.theme.MatteSlateCard
import com.clippulse.studio.ui.theme.MultiSignalOrange
import com.clippulse.studio.ui.theme.SuperChatGold
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary

@Composable
fun ClipCard(
    clip: ClipCandidate,
    isFocused: Boolean,
    onToggleSelected: () -> Unit,
    onNudgeStart: (Double) -> Unit,
    onNudgeEnd: (Double) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember(clip.id) { mutableStateOf(isFocused || clip.superChat != null) }

    val borderColor = when {
        isFocused -> ElectricIndigo
        clip.selected -> ElectricIndigo.copy(alpha = 0.55f)
        else -> HairlineBorder
    }

    Surface(
        modifier = modifier
            .fillMaxWidth()
            .clickable { expanded = !expanded },
        shape = RoundedCornerShape(14.dp),
        color = MatteSlateCard,
        border = BorderStroke(if (isFocused) 1.5.dp else 1.dp, borderColor)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                Checkbox(
                    checked = clip.selected,
                    onCheckedChange = { onToggleSelected() },
                    colors = CheckboxDefaults.colors(
                        checkedColor = ElectricIndigo,
                        uncheckedColor = TextMuted
                    )
                )

                Column(modifier = Modifier.weight(1f)) {
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        if (clip.isMultiSignal) {
                            SignalBadgePill(
                                text = "Multi-Signal",
                                color = MultiSignalOrange,
                                showFire = true
                            )
                        }
                        clip.signals.forEach { signal ->
                            SignalBadgePill(
                                text = signal.label,
                                color = signalBadgeColor(signal),
                                showFire = false
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    Text(
                        text = clip.title,
                        color = TextPrimary,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )

                    Spacer(modifier = Modifier.height(3.dp))

                    Text(
                        text = "${TimeUtils.formatTimestamp(clip.startSec)} - ${TimeUtils.formatTimestamp(clip.endSec)}  •  ${clip.durationSec.toInt()}s",
                        color = TextSecondary,
                        fontSize = 12.sp
                    )
                }

                Spacer(modifier = Modifier.width(8.dp))

                Column(horizontalAlignment = Alignment.End) {
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(ElectricIndigo.copy(alpha = 0.16f))
                            .border(1.dp, ElectricIndigo.copy(alpha = 0.45f), RoundedCornerShape(8.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text(
                            text = "${clip.score}",
                            color = Color.White,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                    IconButton(
                        onClick = { expanded = !expanded },
                        modifier = Modifier.size(28.dp)
                    ) {
                        Icon(
                            imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                            contentDescription = "Expand clip details",
                            tint = TextSecondary
                        )
                    }
                }
            }

            if (clip.superChat != null) {
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(10.dp))
                        .background(SuperChatGold.copy(alpha = 0.12f))
                        .border(1.dp, SuperChatGold.copy(alpha = 0.45f), RoundedCornerShape(10.dp))
                        .padding(horizontal = 10.dp, vertical = 8.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.MonetizationOn,
                        contentDescription = null,
                        tint = SuperChatGold,
                        modifier = Modifier.size(18.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "${clip.superChat.authorName}  •  ${clip.superChat.amountText}",
                            color = SuperChatGold,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                        if (clip.superChat.message.isNotBlank()) {
                            Text(
                                text = clip.superChat.message,
                                color = TextPrimary,
                                fontSize = 12.sp,
                                maxLines = if (expanded) 5 else 2,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                    }
                }
            }

            AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.padding(top = 10.dp)) {
                    HorizontalDivider(color = HairlineBorder)
                    Spacer(modifier = Modifier.height(8.dp))

                    if (clip.reason.isNotBlank()) {
                        Text(
                            text = clip.reason,
                            color = AiPickCyan,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Medium
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                    }

                    if (clip.transcriptSnippet.isNotBlank()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(ElevatedSlate)
                                .padding(8.dp)
                        ) {
                            Text(
                                text = "\"${clip.transcriptSnippet}\"",
                                color = TextSecondary,
                                fontSize = 12.sp,
                                lineHeight = 16.sp
                            )
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        TrimNudgeGroup(
                            label = "Start ${TimeUtils.formatTimestamp(clip.startSec)}",
                            onMinusTwo = { onNudgeStart(-2.0) },
                            onPlusTwo = { onNudgeStart(2.0) },
                            modifier = Modifier.weight(1f)
                        )
                        TrimNudgeGroup(
                            label = "End ${TimeUtils.formatTimestamp(clip.endSec)}",
                            onMinusTwo = { onNudgeEnd(-2.0) },
                            onPlusTwo = { onNudgeEnd(2.0) },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun TrimNudgeGroup(
    label: String,
    onMinusTwo: () -> Unit,
    onPlusTwo: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier
            .clip(RoundedCornerShape(10.dp))
            .background(ElevatedSlate)
            .border(1.dp, HairlineBorder, RoundedCornerShape(10.dp))
            .padding(6.dp)
    ) {
        Text(text = label, color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Medium)
        Spacer(modifier = Modifier.height(4.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            OutlinedButton(
                onClick = onMinusTwo,
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp),
                shape = RoundedCornerShape(6.dp),
                border = BorderStroke(1.dp, HairlineBorder),
                modifier = Modifier.height(28.dp)
            ) {
                Text("-2s", color = TextPrimary, fontSize = 11.sp)
            }
            OutlinedButton(
                onClick = onPlusTwo,
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp),
                shape = RoundedCornerShape(6.dp),
                border = BorderStroke(1.dp, HairlineBorder),
                modifier = Modifier.height(28.dp)
            ) {
                Text("+2s", color = TextPrimary, fontSize = 11.sp)
            }
        }
    }
}

@Composable
private fun SignalBadgePill(
    text: String,
    color: Color,
    showFire: Boolean
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .clip(RoundedCornerShape(6.dp))
            .background(color.copy(alpha = 0.16f))
            .border(1.dp, color.copy(alpha = 0.45f), RoundedCornerShape(6.dp))
            .padding(horizontal = 6.dp, vertical = 2.dp)
    ) {
        if (showFire) {
            Icon(
                imageVector = Icons.Default.LocalFireDepartment,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(12.dp)
            )
            Spacer(modifier = Modifier.width(2.dp))
        }
        Text(
            text = text,
            color = color,
            fontSize = 10.sp,
            fontWeight = FontWeight.SemiBold
        )
    }
}

private fun signalBadgeColor(signal: SignalType): Color {
    return when (signal) {
        SignalType.SUPER_CHAT -> SuperChatGold
        SignalType.HEATMAP -> HeatmapCrimson
        SignalType.CHAT_HYPE -> ChatHypePurple
        SignalType.AI_PICK -> AiPickCyan
        SignalType.AUDIO_PEAK -> ElectricIndigo
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/ui/components/AiManagerSheet.kt"] = r'''@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)

package com.clippulse.studio.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.AiProviderPreset
import com.clippulse.studio.ui.StudioUiState
import com.clippulse.studio.ui.theme.AiPickCyan
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.HeatmapCrimson
import com.clippulse.studio.ui.theme.MatteSlateCard
import com.clippulse.studio.ui.theme.SuccessGreen
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary

@Composable
fun AiManagerSheet(
    state: StudioUiState,
    onDismiss: () -> Unit,
    onSelectPreset: (AiProviderPreset) -> Unit,
    onBaseUrlChanged: (String) -> Unit,
    onPrimaryKeyChanged: (String) -> Unit,
    onAddBackupKey: (String) -> Unit,
    onRemoveBackupKey: (String) -> Unit,
    onSelectModel: (String) -> Unit,
    onFetchModels: () -> Unit,
    onConnect: () -> Unit,
    onToggleSmartPeak: (Boolean) -> Unit,
    onToggleOfflineMode: (Boolean) -> Unit,
    onUpdateYtDlp: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showKey by remember { mutableStateOf(false) }
    var newBackupKeyInput by remember { mutableStateOf("") }
    var modelDropdownExpanded by remember { mutableStateOf(false) }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = MatteSlateCard
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 8.dp)
        ) {
            Text(
                text = "Universal AI API & Engine Manager",
                color = TextPrimary,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "Connect any OpenAI-compatible endpoint or run 100% offline.",
                color = TextSecondary,
                fontSize = 12.sp
            )

            Spacer(modifier = Modifier.height(14.dp))

            SettingSwitchRow(
                title = "100% Offline / No-AI Mode",
                subtitle = "Run Heatmap, Super Chat, Chat Velocity & Audio Peaks with zero API keys",
                checked = state.aiSettings.offlineMode,
                onCheckedChange = onToggleOfflineMode
            )

            Spacer(modifier = Modifier.height(8.dp))

            SettingSwitchRow(
                title = "Smart Peak-Only Mode (~85% Token Savings)",
                subtitle = "Slices only 2-minute caption windows around detected peaks/Super Chats",
                checked = state.aiSettings.smartPeakOnly,
                onCheckedChange = onToggleSmartPeak
            )

            Spacer(modifier = Modifier.height(14.dp))
            HorizontalDivider(color = HairlineBorder)
            Spacer(modifier = Modifier.height(14.dp))

            Text("API Provider Presets", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(6.dp))
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                AiProviderPreset.entries.forEach { preset ->
                    FilterChip(
                        selected = state.aiSettings.preset == preset,
                        onClick = { onSelectPreset(preset) },
                        label = { Text(preset.displayName, fontSize = 12.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = ElectricIndigo,
                            selectedLabelColor = Color.White,
                            containerColor = ElevatedSlate,
                            labelColor = TextSecondary
                        )
                    )
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            OutlinedTextField(
                value = state.aiSettings.baseUrl,
                onValueChange = onBaseUrlChanged,
                label = { Text("Base URL") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(10.dp))

            OutlinedTextField(
                value = state.aiSettings.primaryApiKey,
                onValueChange = onPrimaryKeyChanged,
                label = { Text("Primary API Key") },
                singleLine = true,
                visualTransformation = if (showKey) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = { showKey = !showKey }) {
                        Icon(
                            imageVector = if (showKey) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                            contentDescription = "Toggle API key visibility",
                            tint = TextSecondary
                        )
                    }
                },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = "Backup Failover Keys (${state.aiSettings.backupApiKeys.size})",
                color = TextSecondary,
                fontSize = 12.sp,
                fontWeight = FontWeight.SemiBold
            )
            Text(
                text = "Auto-rotates on HTTP 429 rate limits or 401 auth errors.",
                color = TextSecondary,
                fontSize = 11.sp
            )
            Spacer(modifier = Modifier.height(6.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = newBackupKeyInput,
                    onValueChange = { newBackupKeyInput = it },
                    placeholder = { Text("Add failover key...", fontSize = 12.sp) },
                    singleLine = true,
                    modifier = Modifier.weight(1f)
                )
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(
                    onClick = {
                        onAddBackupKey(newBackupKeyInput)
                        newBackupKeyInput = ""
                    },
                    modifier = Modifier
                        .clip(RoundedCornerShape(10.dp))
                        .background(ElectricIndigo)
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add backup key", tint = Color.White)
                }
            }

            state.aiSettings.backupApiKeys.forEach { backupKey ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 6.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(ElevatedSlate)
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    val masked = if (backupKey.length > 8) {
                        "${backupKey.take(4)}••••${backupKey.takeLast(4)}"
                    } else {
                        "••••••••"
                    }
                    Text(masked, color = TextPrimary, fontSize = 12.sp)
                    IconButton(onClick = { onRemoveBackupKey(backupKey) }, modifier = Modifier.size(28.dp)) {
                        Icon(
                            Icons.Default.Delete,
                            contentDescription = "Remove backup key",
                            tint = HeatmapCrimson,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            Text("Model Selection", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(6.dp))

            Box(modifier = Modifier.fillMaxWidth()) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(10.dp))
                        .background(ElevatedSlate)
                        .border(1.dp, HairlineBorder, RoundedCornerShape(10.dp))
                        .clickable { modelDropdownExpanded = true }
                        .padding(horizontal = 12.dp, vertical = 14.dp)
                ) {
                    Text(
                        text = state.aiSettings.selectedModel.ifBlank { "Select a model" },
                        color = TextPrimary,
                        fontSize = 13.sp,
                        modifier = Modifier.weight(1f)
                    )
                    Icon(Icons.Default.ArrowDropDown, contentDescription = null, tint = TextSecondary)
                }

                DropdownMenu(
                    expanded = modelDropdownExpanded,
                    onDismissRequest = { modelDropdownExpanded = false }
                ) {
                    state.aiSettings.availableModels.forEach { modelId ->
                        DropdownMenuItem(
                            text = { Text(modelId, fontSize = 13.sp) },
                            onClick = {
                                onSelectModel(modelId)
                                modelDropdownExpanded = false
                            }
                        )
                    }
                }
            }

            if (!state.modelFetchMessage.isNullOrBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = state.modelFetchMessage,
                    color = AiPickCyan,
                    fontSize = 11.sp
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                OutlinedButton(
                    onClick = onFetchModels,
                    enabled = !state.isFetchingModels,
                    shape = RoundedCornerShape(10.dp),
                    border = BorderStroke(1.dp, ElectricIndigo),
                    modifier = Modifier.weight(1f)
                ) {
                    if (state.isFetchingModels) {
                        CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                    } else {
                        Icon(Icons.Default.Refresh, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Fetch Models", fontSize = 12.sp)
                    }
                }

                Button(
                    onClick = onConnect,
                    enabled = state.aiConnectionState !is AiConnectionState.Testing,
                    shape = RoundedCornerShape(10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                    modifier = Modifier.weight(1f)
                ) {
                    if (state.aiConnectionState is AiConnectionState.Testing) {
                        CircularProgressIndicator(
                            color = Color.White,
                            modifier = Modifier.size(16.dp),
                            strokeWidth = 2.dp
                        )
                    } else {
                        Icon(Icons.Default.CheckCircle, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Connect", fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(10.dp))
            when (val conn = state.aiConnectionState) {
                is AiConnectionState.Connected -> {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(SuccessGreen.copy(alpha = 0.15f))
                            .border(1.dp, SuccessGreen.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                            .padding(10.dp)
                    ) {
                        Text(
                            text = "✓ Connected (${conn.latencyMs} ms) • ${conn.model}",
                            color = SuccessGreen,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
                is AiConnectionState.Error -> {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(HeatmapCrimson.copy(alpha = 0.15f))
                            .border(1.dp, HeatmapCrimson.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                            .padding(10.dp)
                    ) {
                        Text(
                            text = conn.message,
                            color = HeatmapCrimson,
                            fontSize = 12.sp
                        )
                    }
                }
                else -> Unit
            }

            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider(color = HairlineBorder)
            Spacer(modifier = Modifier.height(14.dp))

            Text("Extractor Engine Maintenance", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(6.dp))
            OutlinedButton(
                onClick = onUpdateYtDlp,
                enabled = !state.isUpdatingYtDlp,
                shape = RoundedCornerShape(10.dp),
                border = BorderStroke(1.dp, AiPickCyan),
                modifier = Modifier.fillMaxWidth()
            ) {
                if (state.isUpdatingYtDlp) {
                    CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                    Spacer(modifier = Modifier.width(8.dp))
                }
                Text("Update yt-dlp Engine (No APK Rebuild Needed)", color = AiPickCyan, fontSize = 12.sp)
            }
            if (!state.ytDlpUpdateMessage.isNullOrBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(state.ytDlpUpdateMessage, color = TextSecondary, fontSize = 11.sp)
            }

            Spacer(modifier = Modifier.height(28.dp))
        }
    }
}

@Composable
private fun SettingSwitchRow(
    title: String,
    subtitle: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(ElevatedSlate)
            .padding(horizontal = 12.dp, vertical = 8.dp)
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = TextPrimary, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
            Text(subtitle, color = TextSecondary, fontSize = 11.sp, lineHeight = 14.sp)
        }
        Spacer(modifier = Modifier.width(8.dp))
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(checkedTrackColor = ElectricIndigo)
        )
    }
}
'''

FILES["app/src/main/java/com/clippulse/studio/ui/ClipPulseScreen.kt"] = r'''@file:OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)

package com.clippulse.studio.ui

import android.content.ClipboardManager
import android.content.Context
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.ContentCut
import androidx.compose.material.icons.filled.ContentPaste
import androidx.compose.material.icons.filled.CropPortrait
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.VideoFile
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.R
import com.clippulse.studio.engine.TimeUtils
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.ExportProgressState
import com.clippulse.studio.ui.components.AiManagerSheet
import com.clippulse.studio.ui.components.ClipCard
import com.clippulse.studio.ui.components.HeatmapTimeline
import com.clippulse.studio.ui.theme.AiPickCyan
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.HeatmapCrimson
import com.clippulse.studio.ui.theme.MatteSlateCard
import com.clippulse.studio.ui.theme.ObsidianBg
import com.clippulse.studio.ui.theme.SuccessGreen
import com.clippulse.studio.ui.theme.SuperChatGold
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary

@Composable
fun ClipPulseScreen(viewModel: ClipPulseViewModel) {
    val state by viewModel.uiState.collectAsState()
    val exportState by viewModel.exportProgress.collectAsState()
    val context = LocalContext.current

    val localVideoPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            viewModel.onLocalVideoSelected(uri)
        }
    }

    val analysis = state.analysisResult
    val visibleClips = analysis?.clips?.filter {
        viewModel.matchesFilter(it, state.activeFilter)
    }.orEmpty()
    val selectedCount = analysis?.clips?.count { it.selected } ?: 0

    Scaffold(
        containerColor = ObsidianBg,
        topBar = {
            StudioTopBar(
                state = state,
                onOpenAiManager = { viewModel.toggleAiManagerSheet(true) }
            )
        },
        bottomBar = {
            if (analysis != null && analysis.clips.isNotEmpty()) {
                StickyExportDock(
                    selectedCount = selectedCount,
                    useVerticalCrop = state.exportConfig.useVerticalCrop,
                    includeTxtSidecar = state.exportConfig.includeTxtSidecar,
                    exportState = exportState,
                    onToggleVerticalCrop = { vertical ->
                        viewModel.updateExportConfig { it.copy(useVerticalCrop = vertical) }
                    },
                    onToggleTxtSidecar = {
                        viewModel.updateExportConfig { it.copy(includeTxtSidecar = !it.includeTxtSidecar) }
                    },
                    onExportClicked = { viewModel.exportSelectedClips() }
                )
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 14.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            contentPadding = PaddingValues(top = 8.dp, bottom = 24.dp)
        ) {
            item {
                SourceInputCard(
                    state = state,
                    onUrlChanged = viewModel::onUrlChanged,
                    onPasteClick = {
                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as? ClipboardManager
                        val clipText = clipboard?.primaryClip?.getItemAt(0)?.text?.toString().orEmpty()
                        if (clipText.isNotBlank()) {
                            viewModel.onUrlChanged(TimeUtils.extractUrlFromSharedText(clipText))
                        }
                    },
                    onPickLocalClick = { localVideoPicker.launch("video/*") },
                    onModeSelected = viewModel::onDetectionModeSelected,
                    onCustomQueryChanged = viewModel::onCustomAiQueryChanged,
                    onMinSuperChatChanged = viewModel::onMinSuperChatChanged,
                    onPaddingChanged = { startPad, endPad ->
                        viewModel.updateExportConfig {
                            it.copy(startPaddingSec = startPad, endPaddingSec = endPad)
                        }
                    },
                    onAnalyzeClick = viewModel::startAnalysis
                )
            }

            if (analysis != null) {
                item {
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = MatteSlateCard,
                        border = BorderStroke(1.dp, HairlineBorder),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            Text(
                                text = analysis.title,
                                color = TextPrimary,
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold,
                                maxLines = 2,
                                overflow = TextOverflow.Ellipsis
                            )
                            Text(
                                text = "${analysis.channelName}  •  ${TimeUtils.formatTimestamp(analysis.durationSec)}  •  ${analysis.superChatCount} Super Chats",
                                color = TextSecondary,
                                fontSize = 11.sp
                            )

                            Spacer(modifier = Modifier.height(12.dp))

                            HeatmapTimeline(
                                durationSec = analysis.durationSec,
                                heatmap = analysis.heatmap,
                                clips = analysis.clips,
                                focusedClipId = state.focusedClipId,
                                onSelectClipFromTimeline = { clipId ->
                                    viewModel.onFocusClip(clipId)
                                }
                            )

                            Spacer(modifier = Modifier.height(10.dp))

                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .horizontalScroll(rememberScrollState())
                            ) {
                                SignalFilter.entries.forEach { filter ->
                                    FilterChip(
                                        selected = state.activeFilter == filter,
                                        onClick = { viewModel.onSignalFilterSelected(filter) },
                                        label = { Text(filter.label, fontSize = 11.sp) },
                                        colors = FilterChipDefaults.filterChipColors(
                                            selectedContainerColor = ElectricIndigo,
                                            selectedLabelColor = Color.White,
                                            containerColor = ElevatedSlate,
                                            labelColor = TextSecondary
                                        ),
                                        modifier = Modifier.padding(end = 6.dp)
                                    )
                                }
                            }

                            Row(
                                horizontalArrangement = Arrangement.End,
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                TextButton(onClick = { viewModel.selectAllVisibleClips(true) }) {
                                    Text("Select All", color = AiPickCyan, fontSize = 12.sp)
                                }
                                TextButton(onClick = { viewModel.selectAllVisibleClips(false) }) {
                                    Text("Clear", color = TextSecondary, fontSize = 12.sp)
                                }
                            }
                        }
                    }
                }

                if (visibleClips.isEmpty()) {
                    item {
                        Box(
                            contentAlignment = Alignment.Center,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(14.dp))
                                .background(MatteSlateCard)
                                .border(1.dp, HairlineBorder, RoundedCornerShape(14.dp))
                                .padding(24.dp)
                        ) {
                            Text(
                                text = "No clips match the active filter. Switch to 'All' or try another detection mode.",
                                color = TextSecondary,
                                fontSize = 13.sp
                            )
                        }
                    }
                } else {
                    items(visibleClips, key = { it.id }) { clip ->
                        ClipCard(
                            clip = clip,
                            isFocused = clip.id == state.focusedClipId,
                            onToggleSelected = { viewModel.toggleClipSelection(clip.id) },
                            onNudgeStart = { delta -> viewModel.nudgeClipStart(clip.id, delta) },
                            onNudgeEnd = { delta -> viewModel.nudgeClipEnd(clip.id, delta) }
                        )
                    }
                }
            }
        }
    }

    if (state.showAiManagerSheet) {
        AiManagerSheet(
            state = state,
            onDismiss = { viewModel.toggleAiManagerSheet(false) },
            onSelectPreset = viewModel::selectAiPreset,
            onBaseUrlChanged = { url -> viewModel.updateAiSettings { it.copy(baseUrl = url) } },
            onPrimaryKeyChanged = { key -> viewModel.updateAiSettings { it.copy(primaryApiKey = key) } },
            onAddBackupKey = viewModel::addBackupKey,
            onRemoveBackupKey = viewModel::removeBackupKey,
            onSelectModel = { model -> viewModel.updateAiSettings { it.copy(selectedModel = model) } },
            onFetchModels = viewModel::fetchModels,
            onConnect = viewModel::connectAiModel,
            onToggleSmartPeak = { enabled -> viewModel.updateAiSettings { it.copy(smartPeakOnly = enabled) } },
            onToggleOfflineMode = { offline -> viewModel.updateAiSettings { it.copy(offlineMode = offline) } },
            onUpdateYtDlp = viewModel::updateYtDlpEngine
        )
    }
}

@Composable
private fun StudioTopBar(
    state: StudioUiState,
    onOpenAiManager: () -> Unit
) {
    val connState = state.aiConnectionState
    val (pillText, pillColor) = when {
        state.aiSettings.offlineMode -> "Offline Mode" to TextSecondary
        connState is AiConnectionState.Connected ->
            "✓ Connected (${connState.latencyMs}ms)" to SuccessGreen
        connState is AiConnectionState.Error ->
            "AI Error" to HeatmapCrimson
        state.aiSettings.primaryApiKey.isNotBlank() ->
            state.aiSettings.selectedModel.take(16) to AiPickCyan
        else -> "AI Setup" to SuperChatGold
    }

    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween,
        modifier = Modifier
            .fillMaxWidth()
            .background(ObsidianBg)
            .statusBarsPadding()
            .padding(horizontal = 14.dp, vertical = 10.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                painter = painterResource(id = R.drawable.ic_launcher),
                contentDescription = "ClipPulse Logo",
                tint = Color.Unspecified,
                modifier = Modifier
                    .size(32.dp)
                    .clip(RoundedCornerShape(8.dp))
            )
            Spacer(modifier = Modifier.width(10.dp))
            Column {
                Text(
                    text = "ClipPulse",
                    color = TextPrimary,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "Zero-Download Clip Studio",
                    color = TextMuted,
                    fontSize = 10.sp
                )
            }
        }

        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .clip(CircleShape)
                .background(MatteSlateCard)
                .border(1.dp, pillColor.copy(alpha = 0.55f), CircleShape)
                .clickable { onOpenAiManager() }
                .padding(horizontal = 12.dp, vertical = 7.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(7.dp)
                    .clip(CircleShape)
                    .background(pillColor)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = pillText,
                color = pillColor,
                fontSize = 11.sp,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.width(4.dp))
            Icon(
                imageVector = Icons.Default.Settings,
                contentDescription = "Open AI Settings",
                tint = TextSecondary,
                modifier = Modifier.size(14.dp)
            )
        }
    }
}

@Composable
private fun SourceInputCard(
    state: StudioUiState,
    onUrlChanged: (String) -> Unit,
    onPasteClick: () -> Unit,
    onPickLocalClick: () -> Unit,
    onModeSelected: (DetectionMode) -> Unit,
    onCustomQueryChanged: (String) -> Unit,
    onMinSuperChatChanged: (Double) -> Unit,
    onPaddingChanged: (Int, Int) -> Unit,
    onAnalyzeClick: () -> Unit
) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = MatteSlateCard,
        border = BorderStroke(1.dp, HairlineBorder),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = if (state.selectedLocalUri != null) state.selectedLocalName else state.urlInput,
                    onValueChange = onUrlChanged,
                    placeholder = {
                        Text(
                            "Paste YouTube, VOD, or Facebook URL...",
                            fontSize = 12.sp,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    },
                    singleLine = true,
                    trailingIcon = {
                        IconButton(onClick = onPasteClick) {
                            Icon(
                                imageVector = Icons.Default.ContentPaste,
                                contentDescription = "Paste URL",
                                tint = AiPickCyan
                            )
                        }
                    },
                    modifier = Modifier.weight(1f)
                )

                Spacer(modifier = Modifier.width(8.dp))

                OutlinedButton(
                    onClick = onPickLocalClick,
                    shape = RoundedCornerShape(10.dp),
                    border = BorderStroke(1.dp, HairlineBorder),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 14.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.VideoFile,
                        contentDescription = "Pick local video",
                        tint = ElectricIndigo,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                DetectionMode.entries.forEach { mode ->
                    FilterChip(
                        selected = state.detectionMode == mode,
                        onClick = { onModeSelected(mode) },
                        label = { Text(mode.label, fontSize = 11.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = ElectricIndigo,
                            selectedLabelColor = Color.White,
                            containerColor = ElevatedSlate,
                            labelColor = TextSecondary
                        )
                    )
                }
            }

            if (!state.aiSettings.offlineMode &&
                (state.detectionMode == DetectionMode.AI_VIRAL || state.detectionMode == DetectionMode.ALL)
            ) {
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = state.customAiQuery,
                    onValueChange = onCustomQueryChanged,
                    placeholder = {
                        Text(
                            "Optional AI prompt (e.g., \"every rage moment\")",
                            fontSize = 12.sp
                        )
                    },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }

            Spacer(modifier = Modifier.height(8.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
            ) {
                val minOptions = listOf(0.0 to "All Donations", 5.0 to "$5+ SC", 10.0 to "$10+ SC", 25.0 to "$25+ SC")
                minOptions.forEach { (amount, label) ->
                    FilterChip(
                        selected = state.minSuperChatUsd == amount,
                        onClick = { onMinSuperChatChanged(amount) },
                        label = { Text(label, fontSize = 10.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = SuperChatGold.copy(alpha = 0.25f),
                            selectedLabelColor = SuperChatGold,
                            containerColor = ElevatedSlate,
                            labelColor = TextSecondary
                        )
                    )
                }

                val padPresets = listOf(
                    Triple(3, 5, "Pad -3s/+5s"),
                    Triple(5, 8, "Pad -5s/+8s"),
                    Triple(0, 0, "Exact 0s")
                )
                padPresets.forEach { (sPad, ePad, label) ->
                    val active = state.exportConfig.startPaddingSec == sPad &&
                        state.exportConfig.endPaddingSec == ePad
                    FilterChip(
                        selected = active,
                        onClick = { onPaddingChanged(sPad, ePad) },
                        label = { Text(label, fontSize = 10.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = AiPickCyan.copy(alpha = 0.25f),
                            selectedLabelColor = AiPickCyan,
                            containerColor = ElevatedSlate,
                            labelColor = TextSecondary
                        )
                    )
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Button(
                onClick = onAnalyzeClick,
                enabled = !state.isAnalyzing,
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
            ) {
                if (state.isAnalyzing) {
                    CircularProgressIndicator(
                        color = Color.White,
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text("Analyzing...", color = Color.White, fontWeight = FontWeight.SemiBold)
                } else {
                    Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = Color.White)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Analyze & Detect Clips", color = Color.White, fontWeight = FontWeight.Bold)
                }
            }

            if (state.isAnalyzing && state.analysisStepText.isNotBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                LinearProgressIndicator(
                    color = AiPickCyan,
                    trackColor = ElevatedSlate,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = state.analysisStepText,
                    color = AiPickCyan,
                    fontSize = 11.sp
                )
            }

            if (!state.analysisError.isNullOrBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = state.analysisError,
                    color = HeatmapCrimson,
                    fontSize = 12.sp
                )
            }
        }
    }
}

@Composable
private fun StickyExportDock(
    selectedCount: Int,
    useVerticalCrop: Boolean,
    includeTxtSidecar: Boolean,
    exportState: ExportProgressState,
    onToggleVerticalCrop: (Boolean) -> Unit,
    onToggleTxtSidecar: () -> Unit,
    onExportClicked: () -> Unit
) {
    Surface(
        color = MatteSlateCard,
        border = BorderStroke(1.dp, HairlineBorder),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .navigationBarsPadding()
                .padding(horizontal = 14.dp, vertical = 10.dp)
        ) {
            if (exportState.isExporting || exportState.statusMessage.isNotBlank()) {
                if (exportState.isExporting) {
                    LinearProgressIndicator(
                        progress = { exportState.fraction.coerceIn(0f, 1f) },
                        color = SuccessGreen,
                        trackColor = ElevatedSlate,
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                }
                Text(
                    text = exportState.statusMessage,
                    color = if (exportState.errorMessage != null) HeatmapCrimson else SuccessGreen,
                    fontSize = 11.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(6.dp))
            }

            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                FilterChip(
                    selected = !useVerticalCrop,
                    onClick = { onToggleVerticalCrop(false) },
                    leadingIcon = {
                        Icon(Icons.Default.ContentCut, contentDescription = null, modifier = Modifier.size(14.dp))
                    },
                    label = { Text("Fast Cut", fontSize = 11.sp) },
                    colors = FilterChipDefaults.filterChipColors(
                        selectedContainerColor = ElectricIndigo.copy(alpha = 0.3f),
                        selectedLabelColor = Color.White,
                        containerColor = ElevatedSlate,
                        labelColor = TextSecondary
                    )
                )

                FilterChip(
                    selected = useVerticalCrop,
                    onClick = { onToggleVerticalCrop(true) },
                    leadingIcon = {
                        Icon(Icons.Default.CropPortrait, contentDescription = null, modifier = Modifier.size(14.dp))
                    },
                    label = { Text("9:16 Crop", fontSize = 11.sp) },
                    colors = FilterChipDefaults.filterChipColors(
                        selectedContainerColor = ElectricIndigo.copy(alpha = 0.3f),
                        selectedLabelColor = Color.White,
                        containerColor = ElevatedSlate,
                        labelColor = TextSecondary
                    )
                )

                FilterChip(
                    selected = includeTxtSidecar,
                    onClick = onToggleTxtSidecar,
                    leadingIcon = {
                        Icon(Icons.Default.Description, contentDescription = null, modifier = Modifier.size(14.dp))
                    },
                    label = { Text("+.TXT", fontSize = 11.sp) },
                    colors = FilterChipDefaults.filterChipColors(
                        selectedContainerColor = AiPickCyan.copy(alpha = 0.25f),
                        selectedLabelColor = AiPickCyan,
                        containerColor = ElevatedSlate,
                        labelColor = TextSecondary
                    )
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Button(
                onClick = onExportClicked,
                enabled = selectedCount > 0 && !exportState.isExporting,
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(46.dp)
            ) {
                Icon(Icons.Default.Download, contentDescription = null, tint = Color.White)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = if (exportState.isExporting) {
                        "Exporting (${exportState.currentIndex}/${exportState.totalCount})..."
                    } else {
                        "Export Selected Clips to Gallery ($selectedCount)"
                    },
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 13.sp
                )
            }
        }
    }
}
'''

# ==============================================================================
# 9. WRITE ALL PROJECT FILES SAFELY & LINK ANDROID SDK
# ==============================================================================

def main():
    created_count = 0
    for rel_path, content in FILES.items():
        parent = os.path.dirname(rel_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(rel_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content.lstrip("\n"))
        created_count += 1
        print(f"[OK] Generated {rel_path}")

    # Automatically link GitHub Actions pre-installed ANDROID_HOME into local.properties
    sdk_dir = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if sdk_dir and os.path.isdir(sdk_dir):
        escaped_sdk = sdk_dir.replace("\\", "\\\\")
        with open("local.properties", "w", encoding="utf-8", newline="\n") as f:
            f.write(f"sdk.dir={escaped_sdk}\n")
        print(f"[OK] Linked Android SDK in local.properties -> {sdk_dir}")

    print(f"\nSuccessfully generated {created_count} ClipPulse Android project files.")


if __name__ == "__main__":
    main()
