#!/usr/bin/env python3
"""
ClipPulse Android Project Generator
Generates the complete Gradle, Manifest, XML resource, and Kotlin Jetpack Compose
source tree ready for zero-PC compilation on GitHub Actions.
"""

import os
import sys


def write_file(path: str, content: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))
    print(f"Wrote: {path}")


def generate_local_properties() -> None:
    sdk_dir = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if sdk_dir:
        escaped = sdk_dir.replace("\\", "\\\\")
        write_file("local.properties", f"sdk.dir={escaped}\n")
    else:
        print("Note: ANDROID_HOME / ANDROID_SDK_ROOT not set; skipped local.properties.")


def generate_gradle_files() -> None:
    write_file(
        "gradle.properties",
        """
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",
    )

    write_file(
        "settings.gradle.kts",
        """
pluginManagement {
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
""",
    )

    write_file(
        "build.gradle.kts",
        """
plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
""",
    )

    write_file(
        "app/proguard-rules.pro",
        """
-keep class com.yausername.** { *; }
-dontwarn com.yausername.**
""",
    )

    write_file(
        "app/build.gradle.kts",
        """
plugins {
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
        debug {
            isMinifyEnabled = false
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

    lint {
        abortOnError = false
        checkReleaseBuilds = false
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.10.01")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")

    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("androidx.core:core-ktx:1.13.1")

    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    implementation("androidx.media3:media3-exoplayer:1.4.1")
    implementation("androidx.media3:media3-ui:1.4.1")

    implementation("io.github.junkfood02.youtubedl-android:library:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:ffmpeg:0.18.1")
    implementation("io.github.junkfood02.youtubedl-android:common:0.18.1")
}
""",
    )


def generate_manifest_and_resources() -> None:
    write_file(
        "app/src/main/AndroidManifest.xml",
        """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission
        android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32"
        tools:node="replace" />
    <uses-permission
        android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="29"
        tools:node="replace" />

    <application
        android:name=".ClipPulseApp"
        android:allowBackup="true"
        android:extractNativeLibs="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@drawable/ic_launcher"
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
            android:exported="false"
            android:foregroundServiceType="dataSync" />

    </application>

</manifest>
""",
    )

    write_file(
        "app/src/main/res/drawable/ic_launcher.xml",
        """
<?xml version="1.0" encoding="utf-8"?>
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
        android:pathData="M24,18h60c3.31,0 6,2.69 6,6v60c0,3.31 -2.69,6 -6,6h-60c-3.31,0 -6,-2.69 -6,-6v-60c0,-3.31 2.69,-6 6,-6z" />

    <path
        android:fillColor="#6366F1"
        android:pathData="M26,28h56v52h-56z"
        android:fillAlpha="0.16" />

    <path
        android:fillColor="#6366F1"
        android:pathData="M22,52h11l6,-18l8,36l8,-28l6,16l5,-6h20v6h-17l-9,11l-7,-18l-8,28l-8,-35l-4,14h-11z" />

    <path
        android:fillColor="#F59E0B"
        android:pathData="M78,24l2.2,4.8l5.3,0.6l-3.9,3.6l1.1,5.2l-4.7,-2.6l-4.7,2.6l1.1,-5.2l-3.9,-3.6l5.3,-0.6z" />

    <path
        android:fillColor="#06B6D4"
        android:pathData="M24,24h12v4h-8v8h-4z" />

    <path
        android:fillColor="#06B6D4"
        android:pathData="M84,84h-12v-4h8v-8h4z" />
</vector>
""",
    )

    write_file(
        "app/src/main/res/values/strings.xml",
        """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">ClipPulse</string>
</resources>
""",
    )

    write_file(
        "app/src/main/res/values/themes.xml",
        """
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.ClipPulse" parent="android:Theme.Material.NoActionBar">
        <item name="android:statusBarColor">#0B0B0F</item>
        <item name="android:navigationBarColor">#0B0B0F</item>
        <item name="android:windowBackground">#0B0B0F</item>
    </style>
</resources>
""",
    )


def generate_kotlin_sources() -> None:
    base = "app/src/main/java/com/clippulse/studio"

    write_file(
        f"{base}/ClipPulseApp.kt",
        """
package com.clippulse.studio

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.clippulse.studio.engine.EngineInitializer
import com.clippulse.studio.service.ClipExportService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class ClipPulseApp : Application() {
    private val appScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        appScope.launch {
            EngineInitializer.ensureInitialized(this@ClipPulseApp)
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                ClipExportService.CHANNEL_ID,
                "ClipPulse Exports",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Background section download and gallery export progress"
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }
}
""",
    )

    write_file(
        f"{base}/MainActivity.kt",
        """
package com.clippulse.studio

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import com.clippulse.studio.ui.ClipPulseStudioScreen
import com.clippulse.studio.ui.theme.ClipPulseTheme
import com.clippulse.studio.viewmodel.ClipPulseViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: ClipPulseViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(android.graphics.Color.parseColor("#0B0B0F")),
            navigationBarStyle = SystemBarStyle.dark(android.graphics.Color.parseColor("#0B0B0F"))
        )
        super.onCreate(savedInstanceState)
        handleIncomingIntent(intent)

        setContent {
            ClipPulseTheme {
                ClipPulseStudioScreen(viewModel = viewModel)
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIncomingIntent(intent)
    }

    private fun handleIncomingIntent(incoming: Intent?) {
        if (incoming?.action == Intent.ACTION_SEND && incoming.type == "text/plain") {
            val sharedText = incoming.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
            val urlRegex = Regex("""https?://\\S+""")
            val extractedUrl = urlRegex.find(sharedText)?.value?.trimEnd('.', ',', ')', ']') ?: sharedText.trim()
            if (extractedUrl.isNotBlank()) {
                viewModel.onSharedUrlReceived(extractedUrl)
            }
        }
    }
}
""",
    )

    write_file(
        f"{base}/model/ClipModels.kt",
        """
package com.clippulse.studio.model

import androidx.compose.ui.graphics.Color
import com.clippulse.studio.ui.theme.ColorCrimson
import com.clippulse.studio.ui.theme.ColorCyan
import com.clippulse.studio.ui.theme.ColorEmerald
import com.clippulse.studio.ui.theme.ColorGold
import com.clippulse.studio.ui.theme.ColorPurple
import java.util.Locale

enum class AiPreset(
    val displayName: String,
    val defaultBaseUrl: String,
    val defaultModel: String
) {
    DEEPSEEK("DeepSeek", "https://api.deepseek.com/v1", "deepseek-chat"),
    GEMINI("Gemini", "https://generativelanguage.googleapis.com/v1beta/openai", "gemini-2.5-flash"),
    OPENROUTER("OpenRouter", "https://openrouter.ai/api/v1", "google/gemini-2.5-flash"),
    CUSTOM("Custom", "https://api.openai.com/v1", "gpt-4o-mini")
}

data class AiConfig(
    val preset: AiPreset = AiPreset.DEEPSEEK,
    val baseUrl: String = AiPreset.DEEPSEEK.defaultBaseUrl,
    val primaryKey: String = "",
    val backupKeys: List<String> = emptyList(),
    val selectedModel: String = AiPreset.DEEPSEEK.defaultModel,
    val availableModels: List<String> = listOf(
        "deepseek-chat",
        "deepseek-reasoner",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gpt-4o-mini"
    ),
    val smartPeakOnly: Boolean = true,
    val offlineNoAiMode: Boolean = false
) {
    fun orderedKeys(): List<String> {
        return (listOf(primaryKey.trim()) + backupKeys.map { it.trim() })
            .filter { it.isNotBlank() }
            .distinct()
    }

    fun canUseAi(): Boolean {
        return !offlineNoAiMode && orderedKeys().isNotEmpty() && baseUrl.isNotBlank()
    }
}

sealed class AiConnectionState {
    data object Idle : AiConnectionState()
    data object Testing : AiConnectionState()
    data class Connected(val latencyMs: Long, val model: String) : AiConnectionState()
    data class Error(val message: String) : AiConnectionState()
}

enum class DetectionMode(val label: String) {
    SMART_ALL("All Signals"),
    HEATMAP("Most Replayed"),
    SUPER_CHAT("Super Chats"),
    CHAT_HYPE("Chat Hype"),
    AUDIO_PEAKS("Audio Peaks"),
    AI_CUSTOM("AI Custom Prompt")
}

enum class SignalSource(val label: String, val badgeColor: Color) {
    SUPER_CHAT("Super Chat", ColorGold),
    HEATMAP("Heatmap", ColorCrimson),
    CHAT_HYPE("Chat Hype", ColorPurple),
    AI_PICK("AI Pick", ColorCyan),
    AUDIO_PEAK("Audio Peak", ColorEmerald)
}

enum class SuperChatThreshold(val label: String, val minUsd: Double) {
    ALL("All", 0.0),
    PLUS_5("$5+", 5.0),
    PLUS_10("$10+", 10.0),
    PLUS_25("$25+", 25.0)
}

enum class PaddingPreset(val label: String, val beforeSec: Double, val afterSec: Double) {
    TIGHT("-2s / +3s", 2.0, 3.0),
    BALANCED("-3s / +5s", 3.0, 5.0),
    WIDE("-5s / +8s", 5.0, 8.0),
    CONTEXT("-8s / +12s", 8.0, 12.0)
}

data class HeatmapPoint(
    val startSec: Double,
    val endSec: Double,
    val value: Double
)

data class SuperChatEvent(
    val donor: String,
    val amountDisplay: String,
    val usdApprox: Double,
    val currency: String,
    val message: String,
    val offsetSec: Double
)

data class TranscriptCue(
    val startSec: Double,
    val endSec: Double,
    val text: String
)

data class ClipCandidate(
    val id: String,
    val title: String,
    val startSec: Double,
    val endSec: Double,
    val hypeScore: Int,
    val signals: List<SignalSource>,
    val isMultiSignal: Boolean,
    val superChat: SuperChatEvent? = null,
    val transcriptQuote: String = "",
    val reason: String = "",
    val selected: Boolean = true
) {
    val durationSec: Double
        get() = (endSec - startSec).coerceAtLeast(1.0)
}

data class VideoAnalysisResult(
    val sourceUrlOrUri: String,
    val isLocalFile: Boolean,
    val localFilePath: String?,
    val videoTitle: String,
    val channelName: String,
    val durationSec: Double,
    val heatmap: List<HeatmapPoint>,
    val clips: List<ClipCandidate>,
    val hasLiveChat: Boolean,
    val hasTranscript: Boolean,
    val analysisSummary: String
)

enum class ExportMode(val label: String) {
    FAST_COPY("Fast Cut"),
    VERTICAL_CROP("9:16 Crop")
}

sealed class ExportJobState {
    data object Idle : ExportJobState()
    data class Running(
        val currentIndex: Int,
        val total: Int,
        val currentTitle: String,
        val progressFraction: Float
    ) : ExportJobState()

    data class Completed(
        val exportedCount: Int,
        val savedLocations: List<String>
    ) : ExportJobState()

    data class Failed(val error: String) : ExportJobState()
}

object TimeFormatter {
    fun formatTimestamp(totalSeconds: Double): String {
        val safeSec = totalSeconds.coerceAtLeast(0.0).toLong()
        val hours = safeSec / 3600L
        val minutes = (safeSec % 3600L) / 60L
        val seconds = safeSec % 60L
        return if (hours > 0L) {
            String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds)
        } else {
            String.format(Locale.US, "%02d:%02d", minutes, seconds)
        }
    }

    fun formatFfmpegDuration(totalSeconds: Double): String {
        val clamped = totalSeconds.coerceAtLeast(0.0)
        val hours = (clamped / 3600.0).toInt()
        val minutes = ((clamped % 3600.0) / 60.0).toInt()
        val seconds = clamped % 60.0
        return String.format(Locale.US, "%02d:%02d:%05.2f", hours, minutes, seconds)
    }

    fun formatSectionTimestamp(totalSeconds: Double): String {
        val safeSec = totalSeconds.coerceAtLeast(0.0).toLong()
        val hours = safeSec / 3600L
        val minutes = (safeSec % 3600L) / 60L
        val seconds = safeSec % 60L
        return String.format(Locale.US, "%02d:%02d:%02d", hours, minutes, seconds)
    }
}
""",
    )

    write_file(
        f"{base}/data/AiConfigStore.kt",
        """
package com.clippulse.studio.data

import android.content.Context
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.AiPreset
import org.json.JSONArray

class AiConfigStore(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun load(): AiConfig {
        val presetName = prefs.getString(KEY_PRESET, AiPreset.DEEPSEEK.name) ?: AiPreset.DEEPSEEK.name
        val preset = runCatching { AiPreset.valueOf(presetName) }.getOrDefault(AiPreset.DEEPSEEK)
        val baseUrl = prefs.getString(KEY_BASE_URL, preset.defaultBaseUrl) ?: preset.defaultBaseUrl
        val primaryKey = prefs.getString(KEY_PRIMARY_KEY, "") ?: ""
        val backupKeys = decodeStringList(prefs.getString(KEY_BACKUP_KEYS, "[]") ?: "[]")
        val selectedModel = prefs.getString(KEY_SELECTED_MODEL, preset.defaultModel) ?: preset.defaultModel
        val savedModels = decodeStringList(prefs.getString(KEY_AVAILABLE_MODELS, "[]") ?: "[]")
        val availableModels = if (savedModels.isNotEmpty()) savedModels else AiConfig().availableModels
        val smartPeakOnly = prefs.getBoolean(KEY_SMART_PEAK_ONLY, true)
        val offlineNoAiMode = prefs.getBoolean(KEY_OFFLINE_NO_AI, false)

        return AiConfig(
            preset = preset,
            baseUrl = normalizeBaseUrl(baseUrl),
            primaryKey = primaryKey,
            backupKeys = backupKeys,
            selectedModel = selectedModel,
            availableModels = availableModels,
            smartPeakOnly = smartPeakOnly,
            offlineNoAiMode = offlineNoAiMode
        )
    }

    fun save(config: AiConfig) {
        val normalizedUrl = normalizeBaseUrl(config.baseUrl)
        prefs.edit()
            .putString(KEY_PRESET, config.preset.name)
            .putString(KEY_BASE_URL, normalizedUrl)
            .putString(KEY_PRIMARY_KEY, config.primaryKey.trim())
            .putString(KEY_BACKUP_KEYS, encodeStringList(config.backupKeys.filter { it.isNotBlank() }))
            .putString(KEY_SELECTED_MODEL, config.selectedModel.trim())
            .putString(KEY_AVAILABLE_MODELS, encodeStringList(config.availableModels))
            .putBoolean(KEY_SMART_PEAK_ONLY, config.smartPeakOnly)
            .putBoolean(KEY_OFFLINE_NO_AI, config.offlineNoAiMode)
            .apply()
    }

    private fun encodeStringList(items: List<String>): String {
        val array = JSONArray()
        items.forEach { array.put(it) }
        return array.toString()
    }

    private fun decodeStringList(raw: String): List<String> {
        return try {
            val array = JSONArray(raw)
            buildList {
                for (i in 0 until array.length()) {
                    val value = array.optString(i).trim()
                    if (value.isNotEmpty()) add(value)
                }
            }
        } catch (_: Throwable) {
            emptyList()
        }
    }

    companion object {
        private const val PREFS_NAME = "clippulse_universal_ai_prefs"
        private const val KEY_PRESET = "preset"
        private const val KEY_BASE_URL = "base_url"
        private const val KEY_PRIMARY_KEY = "primary_key"
        private const val KEY_BACKUP_KEYS = "backup_keys"
        private const val KEY_SELECTED_MODEL = "selected_model"
        private const val KEY_AVAILABLE_MODELS = "available_models"
        private const val KEY_SMART_PEAK_ONLY = "smart_peak_only"
        private const val KEY_OFFLINE_NO_AI = "offline_no_ai"

        fun normalizeBaseUrl(rawUrl: String): String {
            var cleaned = rawUrl.trim().trimEnd('/')
            val suffixes = listOf("/chat/completions", "/completions", "/models")
            for (suffix in suffixes) {
                if (cleaned.endsWith(suffix, ignoreCase = true)) {
                    cleaned = cleaned.dropLast(suffix.length).trimEnd('/')
                }
            }
            return cleaned
        }
    }
}
""",
    )

    write_file(
        f"{base}/network/UniversalAiClient.kt",
        """
package com.clippulse.studio.network

import android.os.SystemClock
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TimeFormatter
import com.clippulse.studio.model.TranscriptCue
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.Locale
import java.util.concurrent.TimeUnit

data class AiClipSuggestion(
    val startSec: Double,
    val endSec: Double,
    val title: String,
    val score: Int,
    val reason: String
)

class UniversalAiClient {
    private val client = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(20, TimeUnit.SECONDS)
        .build()

    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    suspend fun fetchModels(config: AiConfig): Result<List<String>> = withContext(Dispatchers.IO) {
        val baseUrl = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        if (baseUrl.isBlank()) {
            return@withContext Result.failure(IllegalArgumentException("Base URL cannot be empty."))
        }
        val keys = config.orderedKeys()
        if (keys.isEmpty()) {
            return@withContext Result.failure(IllegalArgumentException("Enter at least one API key first."))
        }

        val endpoint = "$baseUrl/models"
        val responseResult = executeWithFailover(keys) { key ->
            Request.Builder()
                .url(endpoint)
                .get()
                .addHeader("Authorization", "Bearer $key")
                .addHeader("HTTP-Referer", "https://clippulse.app")
                .addHeader("X-Title", "ClipPulse")
                .build()
        }

        responseResult.mapCatching { body ->
            val root = JSONObject(body)
            val dataArray = root.optJSONArray("data")
                ?: throw IllegalStateException("Response missing 'data' models array.")
            val models = buildList {
                for (i in 0 until dataArray.length()) {
                    val item = dataArray.optJSONObject(i) ?: continue
                    val id = item.optString("id").trim()
                    if (id.isNotEmpty()) add(id)
                }
            }.distinct().sorted()

            if (models.isEmpty()) {
                throw IllegalStateException("Provider returned an empty models list.")
            }
            models
        }
    }

    suspend fun testConnection(config: AiConfig): AiConnectionState = withContext(Dispatchers.IO) {
        val baseUrl = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }

        if (baseUrl.isBlank()) {
            return@withContext AiConnectionState.Error("Base URL is required.")
        }
        if (keys.isEmpty()) {
            return@withContext AiConnectionState.Error("No API key configured.")
        }

        val payload = JSONObject().apply {
            put("model", model)
            put("max_tokens", 1)
            put("temperature", 0.0)
            put("messages", JSONArray().apply {
                put(JSONObject().apply {
                    put("role", "user")
                    put("content", "Hi")
                })
            })
        }.toString()

        val startMs = SystemClock.elapsedRealtime()
        val result = executeWithFailover(keys) { key ->
            Request.Builder()
                .url("$baseUrl/chat/completions")
                .post(payload.toRequestBody(jsonMediaType))
                .addHeader("Authorization", "Bearer $key")
                .addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app")
                .addHeader("X-Title", "ClipPulse")
                .build()
        }
        val elapsedMs = (SystemClock.elapsedRealtime() - startMs).coerceAtLeast(1L)

        result.fold(
            onSuccess = { AiConnectionState.Connected(latencyMs = elapsedMs, model = model) },
            onFailure = { err -> AiConnectionState.Error(err.message ?: "Connection failed") }
        )
    }

    suspend fun findViralAndCustomClips(
        config: AiConfig,
        videoTitle: String,
        durationSec: Double,
        cues: List<TranscriptCue>,
        peakCentersSec: List<Double>,
        customPrompt: String
    ): List<AiClipSuggestion> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || cues.isEmpty()) return@withContext emptyList()

        val transcriptBlock = buildOptimizedTranscriptBlock(
            cues = cues,
            peakCentersSec = peakCentersSec,
            smartPeakOnly = config.smartPeakOnly
        )
        if (transcriptBlock.isBlank()) return@withContext emptyList()

        val goalInstruction = if (customPrompt.isNotBlank()) {
            "Find every moment matching this user request: \"${customPrompt.trim()}\"."
        } else {
            "Identify the top 4 to 8 highest-retention viral hooks, funny moments, heated reactions, or key insights."
        }

        val systemPrompt = """
            You are a viral short-form video editor. Return STRICT JSON ONLY—no markdown fences, no commentary, no reasoning text.
            Schema: {"clips":[{"start":12.5,"end":42.0,"title":"Short punchy title","score":88,"reason":"Why this pops"}]}
            Rules:
            - start and end must be numbers in seconds within [0, ${String.format(Locale.US, "%.1f", durationSec)}].
            - Clip duration should be 12 to 65 seconds.
            - score must be an integer 1 to 100.
        """.trimIndent()

        val userPrompt = """
            Video Title: $videoTitle
            Duration: ${TimeFormatter.formatTimestamp(durationSec)}
            Task: $goalInstruction
            Transcript Segments ([seconds] text):
            $transcriptBlock
        """.trimIndent()

        val rawResponse = completeChat(config, systemPrompt, userPrompt, maxTokens = 900) ?: return@withContext emptyList()
        parseClipSuggestionsJson(rawResponse, durationSec)
    }

    suspend fun alignSuperChatReactions(
        config: AiConfig,
        superChats: List<SuperChatEvent>,
        cues: List<TranscriptCue>,
        durationSec: Double
    ): Map<Double, Pair<Double, Double>> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || superChats.isEmpty() || cues.isEmpty()) return@withContext emptyMap()

        val topDonations = superChats.sortedByDescending { it.usdApprox }.take(8)
        val promptEntries = buildString {
            topDonations.forEachIndexed { index, sc ->
                val windowCues = cues.filter { it.endSec >= sc.offsetSec - 15.0 && it.startSec <= sc.offsetSec + 65.0 }
                val lines = windowCues.joinToString(" ") {
                    "[${String.format(Locale.US, "%.1f", it.startSec)}s] ${it.text}"
                }
                appendLine("Item $index | offset=${String.format(Locale.US, "%.1f", sc.offsetSec)} | donor=${sc.donor} (${sc.amountDisplay}): \"${sc.message}\"")
                appendLine("Transcript around donation: ${lines.take(700)}")
            }
        }

        val systemPrompt = """
            Align each Super Chat donation with the streamer's spoken read & reaction in the transcript.
            Return STRICT JSON ONLY: {"alignments":[{"offset":120.0,"start":116.0,"end":148.0}]}
        """.trimIndent()

        val raw = completeChat(config, systemPrompt, promptEntries, maxTokens = 500) ?: return@withContext emptyMap()
        val cleanJson = extractJsonObject(raw) ?: return@withContext emptyMap()

        return@withContext try {
            val root = JSONObject(cleanJson)
            val arr = root.optJSONArray("alignments") ?: return@withContext emptyMap()
            val map = mutableMapOf<Double, Pair<Double, Double>>()
            for (i in 0 until arr.length()) {
                val obj = arr.optJSONObject(i) ?: continue
                val offset = obj.optDouble("offset", Double.NaN)
                val start = obj.optDouble("start", Double.NaN)
                val end = obj.optDouble("end", Double.NaN)
                if (!offset.isNaN() && !start.isNaN() && !end.isNaN() && end > start) {
                    val safeStart = start.coerceIn(0.0, durationSec)
                    val safeEnd = end.coerceIn(safeStart + 5.0, durationSec.coerceAtLeast(safeStart + 5.0))
                    map[offset] = safeStart to safeEnd
                }
            }
            map
        } catch (_: Throwable) {
            emptyMap()
        }
    }

    private fun buildOptimizedTranscriptBlock(
        cues: List<TranscriptCue>,
        peakCentersSec: List<Double>,
        smartPeakOnly: Boolean
    ): String {
        val selectedCues = if (smartPeakOnly && peakCentersSec.isNotEmpty()) {
            // Slice 2-minute (±60s) windows around detected peaks/Super Chats (~85% token savings)
            cues.filter { cue ->
                peakCentersSec.any { center ->
                    cue.endSec >= (center - 60.0) && cue.startSec <= (center + 60.0)
                }
            }
        } else {
            cues
        }

        val builder = StringBuilder()
        for (cue in selectedCues) {
            val line = "[${String.format(Locale.US, "%.1f", cue.startSec)}] ${cue.text}\n"
            if (builder.length + line.length > 14000) break
            builder.append(line)
        }
        return builder.toString()
    }

    private fun completeChat(
        config: AiConfig,
        systemPrompt: String,
        userPrompt: String,
        maxTokens: Int
    ): String? {
        val baseUrl = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }
        if (baseUrl.isBlank() || keys.isEmpty()) return null

        val payload = JSONObject().apply {
            put("model", model)
            put("max_tokens", maxTokens)
            put("temperature", 0.2)
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
        }.toString()

        val result = executeWithFailover(keys) { key ->
            Request.Builder()
                .url("$baseUrl/chat/completions")
                .post(payload.toRequestBody(jsonMediaType))
                .addHeader("Authorization", "Bearer $key")
                .addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app")
                .addHeader("X-Title", "ClipPulse")
                .build()
        }

        val body = result.getOrNull() ?: return null
        return try {
            val root = JSONObject(body)
            val choices = root.optJSONArray("choices") ?: return null
            if (choices.length() == 0) return null
            val message = choices.getJSONObject(0).optJSONObject("message") ?: return null
            message.optString("content").trim()
        } catch (_: Throwable) {
            null
        }
    }

    private fun parseClipSuggestionsJson(raw: String, durationSec: Double): List<AiClipSuggestion> {
        val jsonText = extractJsonObject(raw) ?: return emptyList()
        return try {
            val root = JSONObject(jsonText)
            val array = root.optJSONArray("clips") ?: return emptyList()
            buildList {
                for (i in 0 until array.length()) {
                    val item = array.optJSONObject(i) ?: continue
                    val start = item.optDouble("start", Double.NaN)
                    val end = item.optDouble("end", Double.NaN)
                    if (start.isNaN() || end.isNaN()) continue
                    val safeStart = start.coerceIn(0.0, (durationSec - 3.0).coerceAtLeast(0.0))
                    val safeEnd = end.coerceIn(safeStart + 4.0, durationSec.coerceAtLeast(safeStart + 4.0))
                    val title = item.optString("title").trim().ifBlank { "AI Viral Highlight #${i + 1}" }
                    val score = item.optInt("score", 82).coerceIn(1, 100)
                    val reason = item.optString("reason").trim().ifBlank { "High-retention moment detected by AI" }
                    add(
                        AiClipSuggestion(
                            startSec = safeStart,
                            endSec = safeEnd,
                            title = title,
                            score = score,
                            reason = reason
                        )
                    )
                }
            }
        } catch (_: Throwable) {
            emptyList()
        }
    }

    private fun extractJsonObject(raw: String): String? {
        // Strip <think>...</think> reasoning blocks and markdown code fences
        val withoutThink = raw.replace(Regex("""<think>[\s\S]*?</think>""", RegexOption.IGNORE_CASE), "")
            .replace("```json", "", ignoreCase = true)
            .replace("```", "")
            .trim()
        val match = Regex("""\{[\s\S]*\}""").find(withoutThink)
        return match?.value
    }

    private fun executeWithFailover(
        keys: List<String>,
        requestFactory: (apiKey: String) -> Request
    ): Result<String> {
        var lastError = "Request failed"
        for ((index, key) in keys.withIndex()) {
            try {
                val request = requestFactory(key)
                client.newCall(request).execute().use { response ->
                    val code = response.code
                    val bodyStr = response.body?.string().orEmpty()
                    if (response.isSuccessful) {
                        return Result.success(bodyStr)
                    }
                    val apiMessage = extractApiErrorMessage(bodyStr, response.message)
                    lastError = "HTTP $code: $apiMessage"

                    val shouldRotate = code == 401 || code == 403 || code == 429 || code in 500..599
                    if (!shouldRotate || index == keys.lastIndex) {
                        return Result.failure(IllegalStateException(lastError))
                    }
                }
            } catch (e: Throwable) {
                lastError = e.message ?: "Network error"
                if (index == keys.lastIndex) {
                    return Result.failure(IllegalStateException(lastError))
                }
            }
        }
        return Result.failure(IllegalStateException(lastError))
    }

    private fun extractApiErrorMessage(body: String, fallback: String): String {
        return try {
            val obj = JSONObject(body)
            val errObj = obj.optJSONObject("error")
            errObj?.optString("message")?.takeIf { it.isNotBlank() }
                ?: obj.optString("message").takeIf { it.isNotBlank() }
                ?: fallback.ifBlank { "API Error" }
        } catch (_: Throwable) {
            body.take(140).ifBlank { fallback.ifBlank { "API Error" } }
        }
    }
}
""",
    )

    write_file(
        f"{base}/engine/EngineInitializer.kt",
        """
package com.clippulse.studio.engine

import android.content.Context
import com.yausername.ffmpeg.FFmpeg
import com.yausername.youtubedl_android.YoutubeDL

object EngineInitializer {
    @Volatile
    private var initialized = false
    private val lock = Any()

    fun ensureInitialized(context: Context): Result<Unit> {
        if (initialized) return Result.success(Unit)
        synchronized(lock) {
            if (initialized) return Result.success(Unit)
            return try {
                val appContext = context.applicationContext
                YoutubeDL.getInstance().init(appContext)
                FFmpeg.getInstance().init(appContext)
                initialized = true
                Result.success(Unit)
            } catch (t: Throwable) {
                Result.failure(t)
            }
        }
    }

    fun updateYtDlpEngine(context: Context): Result<String> {
        return try {
            ensureInitialized(context).getOrThrow()
            val status = YoutubeDL.getInstance().updateYoutubeDL(context.applicationContext)
            Result.success(status?.toString() ?: "UPDATED")
        } catch (t: Throwable) {
            Result.failure(t)
        }
    }
}
""",
    )

    write_file(
        f"{base}/engine/SubtitleAndChatParser.kt",
        """
package com.clippulse.studio.engine

import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TranscriptCue
import org.json.JSONObject
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets
import kotlin.math.sqrt

data class ChatVelocitySpike(
    val startSec: Double,
    val endSec: Double,
    val messageCount: Int,
    val multiplierOverAvg: Double
)

data class LiveChatParseOutput(
    val superChats: List<SuperChatEvent>,
    val velocitySpikes: List<ChatVelocitySpike>,
    val totalMessagesParsed: Int
)

object SubtitleAndChatParser {

    /**
     * RAM-safe line-by-line streaming parser for YouTube .live_chat.json files (100MB+ safe).
     * Extracts Super Chats/Stickers and computes 10-second chat velocity buckets in a single pass.
     */
    fun parseLiveChatStreaming(chatFile: File, durationSec: Double): LiveChatParseOutput {
        if (!chatFile.exists() || chatFile.length() == 0L) {
            return LiveChatParseOutput(emptyList(), emptyList(), 0)
        }

        val superChats = mutableListOf<SuperChatEvent>()
        val bucketCounts = HashMap<Int, Int>()
        var totalMessages = 0

        BufferedReader(
            InputStreamReader(FileInputStream(chatFile), StandardCharsets.UTF_8),
            65536
        ).use { reader ->
            var line: String? = reader.readLine()
            while (line != null) {
                val trimmed = line.trim()
                if (trimmed.startsWith("{")) {
                    parseChatJsonLine(trimmed, durationSec, superChats, bucketCounts)?.let { incremented ->
                        totalMessages += incremented
                    }
                }
                line = reader.readLine()
            }
        }

        val spikes = detectVelocitySpikes(bucketCounts, durationSec)
        return LiveChatParseOutput(
            superChats = superChats.sortedBy { it.offsetSec },
            velocitySpikes = spikes,
            totalMessagesParsed = totalMessages
        )
    }

    private fun parseChatJsonLine(
        jsonLine: String,
        durationSec: Double,
        superChatsOut: MutableList<SuperChatEvent>,
        bucketCountsOut: MutableMap<Int, Int>
    ): Int? {
        return try {
            val root = JSONObject(jsonLine)
            val replayAction = root.optJSONObject("replayChatItemAction") ?: return null
            val offsetMsStr = replayAction.optString("videoOffsetTimeMsec", "")
            val offsetMs = offsetMsStr.toLongOrNull() ?: return null
            if (offsetMs < 0L) return null
            val offsetSec = offsetMs / 1000.0
            if (durationSec > 0.0 && offsetSec > durationSec + 30.0) return null

            val actions = replayAction.optJSONArray("actions") ?: return null
            var counted = 0

            for (i in 0 until actions.length()) {
                val actionObj = actions.optJSONObject(i) ?: continue
                val addItem = actionObj.optJSONObject("addChatItemAction") ?: continue
                val item = addItem.optJSONObject("item") ?: continue

                val bucketIndex = (offsetSec / 10.0).toInt().coerceAtLeast(0)

                val paidMessage = item.optJSONObject("liveChatPaidMessageRenderer")
                val paidSticker = item.optJSONObject("liveChatPaidStickerRenderer")
                val textMessage = item.optJSONObject("liveChatTextMessageRenderer")
                val memberMessage = item.optJSONObject("liveChatMembershipItemRenderer")

                if (paidMessage != null) {
                    counted++
                    bucketCountsOut[bucketIndex] = (bucketCountsOut[bucketIndex] ?: 0) + 1
                    extractSuperChat(paidMessage, offsetSec, isSticker = false)?.let { superChatsOut.add(it) }
                } else if (paidSticker != null) {
                    counted++
                    bucketCountsOut[bucketIndex] = (bucketCountsOut[bucketIndex] ?: 0) + 1
                    extractSuperChat(paidSticker, offsetSec, isSticker = true)?.let { superChatsOut.add(it) }
                } else if (textMessage != null || memberMessage != null) {
                    counted++
                    bucketCountsOut[bucketIndex] = (bucketCountsOut[bucketIndex] ?: 0) + 1
                }
            }
            counted
        } catch (_: Throwable) {
            null
        }
    }

    private fun extractSuperChat(renderer: JSONObject, offsetSec: Double, isSticker: Boolean): SuperChatEvent? {
        val donor = renderer.optJSONObject("authorName")
            ?.optString("simpleText")
            ?.trim()
            ?.takeIf { it.isNotEmpty() }
            ?: "Supporter"

        val amountDisplay = renderer.optJSONObject("purchaseAmountText")
            ?.optString("simpleText")
            ?.trim()
            ?.takeIf { it.isNotEmpty() }
            ?: return null

        val messageRuns = renderer.optJSONObject("message")?.optJSONArray("runs")
        val messageText = buildString {
            if (messageRuns != null) {
                for (i in 0 until messageRuns.length()) {
                    val run = messageRuns.optJSONObject(i) ?: continue
                    append(run.optString("text"))
                }
            }
        }.trim().ifBlank { if (isSticker) "[Super Sticker]" else "" }

        val (currency, usdApprox) = parseCurrencyToUsdApprox(amountDisplay)

        return SuperChatEvent(
            donor = donor,
            amountDisplay = amountDisplay,
            usdApprox = usdApprox,
            currency = currency,
            message = messageText,
            offsetSec = offsetSec
        )
    }

    private fun parseCurrencyToUsdApprox(display: String): Pair<String, Double> {
        val numericStr = display.replace(",", "")
            .let { Regex("""(\d+(?:\.\d+)?)""").find(it)?.groupValues?.getOrNull(1) }
        val rawValue = numericStr?.toDoubleOrNull() ?: 1.0

        return when {
            display.contains("¥") || display.contains("JPY", ignoreCase = true) -> "JPY" to (rawValue / 150.0)
            display.contains("₩") || display.contains("KRW", ignoreCase = true) -> "KRW" to (rawValue / 1380.0)
            display.contains("₹") || display.contains("INR", ignoreCase = true) -> "INR" to (rawValue / 84.0)
            display.contains("€") || display.contains("EUR", ignoreCase = true) -> "EUR" to (rawValue * 1.08)
            display.contains("£") || display.contains("GBP", ignoreCase = true) -> "GBP" to (rawValue * 1.27)
            display.contains("A$") || display.contains("AUD", ignoreCase = true) -> "AUD" to (rawValue * 0.65)
            display.contains("CA$") || display.contains("CAD", ignoreCase = true) -> "CAD" to (rawValue * 0.72)
            display.contains("R$") || display.contains("BRL", ignoreCase = true) -> "BRL" to (rawValue / 5.7)
            display.contains("₱") || display.contains("PHP", ignoreCase = true) -> "PHP" to (rawValue / 58.0)
            else -> "USD" to rawValue
        }
    }

    private fun detectVelocitySpikes(
        bucketCounts: Map<Int, Int>,
        durationSec: Double
    ): List<ChatVelocitySpike> {
        if (bucketCounts.size < 4) return emptyList()

        val values = bucketCounts.values.map { it.toDouble() }
        val mean = values.average()
        val variance = values.sumOf { (it - mean) * (it - mean) } / values.size.toDouble()
        val stdDev = sqrt(variance)
        val threshold = maxOf(6.0, mean + 2.1 * stdDev)

        val spikedBuckets = bucketCounts.entries
            .filter { it.value.toDouble() >= threshold }
            .sortedBy { it.key }

        if (spikedBuckets.isEmpty()) return emptyList()

        val merged = mutableListOf<ChatVelocitySpike>()
        var currentStartBucket = spikedBuckets.first().key
        var currentEndBucket = spikedBuckets.first().key
        var peakCount = spikedBuckets.first().value

        for (i in 1 until spikedBuckets.size) {
            val (bucket, count) = spikedBuckets[i]
            if (bucket <= currentEndBucket + 2) {
                currentEndBucket = bucket
                if (count > peakCount) peakCount = count
            } else {
                merged.add(buildSpike(currentStartBucket, currentEndBucket, peakCount, mean, durationSec))
                currentStartBucket = bucket
                currentEndBucket = bucket
                peakCount = count
            }
        }
        merged.add(buildSpike(currentStartBucket, currentEndBucket, peakCount, mean, durationSec))
        return merged.sortedByDescending { it.messageCount }.take(12)
    }

    private fun buildSpike(
        startBucket: Int,
        endBucket: Int,
        peakCount: Int,
        mean: Double,
        durationSec: Double
    ): ChatVelocitySpike {
        val startSec = (startBucket * 10.0).coerceAtLeast(0.0)
        val rawEnd = (endBucket + 1) * 10.0
        val endSec = if (durationSec > 0.0) rawEnd.coerceAtMost(durationSec) else rawEnd
        val multiplier = if (mean > 0.1) peakCount.toDouble() / mean else 3.0
        return ChatVelocitySpike(
            startSec = startSec,
            endSec = endSec.coerceAtLeast(startSec + 10.0),
            messageCount = peakCount,
            multiplierOverAvg = multiplier
        )
    }

    fun parseVttSubtitles(vttFile: File): List<TranscriptCue> {
        if (!vttFile.exists()) return emptyList()
        val rawCues = mutableListOf<TranscriptCue>()
        val timeRegex = Regex("""(?:(\d+):)?(\d{2}):(\d{2}\.\d+)\s*-->\s*(?:(\d+):)?(\d{2}):(\d{2}\.\d+)""")
        val tagRegex = Regex("""<[^>]+>""")

        var currentStart: Double? = null
        var currentEnd: Double? = null
        val textBuffer = StringBuilder()

        vttFile.forEachLine(StandardCharsets.UTF_8) { rawLine ->
            val line = rawLine.trim()
            val match = timeRegex.find(line)
            if (match != null) {
                val prevStart = currentStart
                val prevEnd = currentEnd
                val prevText = textBuffer.toString().trim()
                if (prevStart != null && prevEnd != null && prevText.isNotEmpty()) {
                    rawCues.add(TranscriptCue(prevStart, prevEnd, prevText))
                }
                textBuffer.clear()
                currentStart = parseVttGroupSeconds(
                    match.groupValues[1],
                    match.groupValues[2],
                    match.groupValues[3]
                )
                currentEnd = parseVttGroupSeconds(
                    match.groupValues[4],
                    match.groupValues[5],
                    match.groupValues[6]
                )
            } else if (
                line.isNotEmpty() &&
                !line.startsWith("WEBVTT") &&
                !line.startsWith("Kind:") &&
                !line.startsWith("Language:") &&
                line.toIntOrNull() == null
            ) {
                val cleaned = line.replace(tagRegex, "")
                    .replace("&amp;", "&")
                    .replace("&gt;", ">")
                    .replace("&lt;", "<")
                    .replace("&#39;", "'")
                    .replace("&quot;", "\"")
                    .trim()
                if (cleaned.isNotEmpty()) {
                    if (textBuffer.isNotEmpty()) textBuffer.append(' ')
                    textBuffer.append(cleaned)
                }
            }
        }

        val lastStart = currentStart
        val lastEnd = currentEnd
        val lastText = textBuffer.toString().trim()
        if (lastStart != null && lastEnd != null && lastText.isNotEmpty()) {
            rawCues.add(TranscriptCue(lastStart, lastEnd, lastText))
        }

        // Deduplicate rolling auto-caption lines
        val deduped = mutableListOf<TranscriptCue>()
        for (cue in rawCues) {
            val prev = deduped.lastOrNull()
            if (prev != null && (prev.text == cue.text || cue.text.startsWith(prev.text))) {
                deduped[deduped.lastIndex] = cue.copy(startSec = prev.startSec)
            } else {
                deduped.add(cue)
            }
        }
        return deduped
    }

    private fun parseVttGroupSeconds(hoursStr: String, minStr: String, secStr: String): Double {
        val h = hoursStr.toDoubleOrNull() ?: 0.0
        val m = minStr.toDoubleOrNull() ?: 0.0
        val s = secStr.toDoubleOrNull() ?: 0.0
        return h * 3600.0 + m * 60.0 + s
    }

    fun extractQuoteAround(cues: List<TranscriptCue>, startSec: Double, endSec: Double): String {
        if (cues.isEmpty()) return ""
        val matching = cues.filter { it.endSec >= startSec && it.startSec <= endSec }
        if (matching.isEmpty()) return ""
        return matching.joinToString(" ") { it.text }.trim().take(220)
    }
}
""",
    )

    write_file(
        f"{base}/engine/VideoAnalysisEngine.kt",
        """
package com.clippulse.studio.engine

import android.content.Context
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.provider.OpenableColumns
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.HeatmapPoint
import com.clippulse.studio.model.PaddingPreset
import com.clippulse.studio.model.SignalSource
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.SuperChatThreshold
import com.clippulse.studio.model.TimeFormatter
import com.clippulse.studio.model.TranscriptCue
import com.clippulse.studio.model.VideoAnalysisResult
import com.clippulse.studio.network.UniversalAiClient
import com.yausername.ffmpeg.FFmpeg
import com.yausername.ffmpeg.FFmpegExecuteRequest
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.util.Locale
import java.util.UUID
import kotlin.math.sqrt

class VideoAnalysisEngine(
    private val aiClient: UniversalAiClient = UniversalAiClient()
) {

    suspend fun analyzeRemoteUrl(
        context: Context,
        rawUrl: String,
        mode: DetectionMode,
        superChatThreshold: SuperChatThreshold,
        paddingPreset: PaddingPreset,
        customAiPrompt: String,
        aiConfig: AiConfig,
        onProgress: (Float, String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            onProgress(0.08f, "Initializing yt-dlp zero-download engine...")
            EngineInitializer.ensureInitialized(context).getOrThrow()

            val workDir = File(context.cacheDir, "analysis_${System.currentTimeMillis()}").apply {
                mkdirs()
            }

            try {
                onProgress(0.22f, "Fetching metadata, heatmap & subtitles (zero video download)...")
                val outputTemplate = File(workDir, "meta.%(ext)s").absolutePath
                val request = YoutubeDLRequest(rawUrl.trim()).apply {
                    addOption("--skip-download")
                    addOption("--write-info-json")
                    addOption("--write-auto-sub")
                    addOption("--write-subs")
                    addOption("--sub-langs", "en.*,live_chat")
                    addOption("--no-playlist")
                    addOption("--no-warnings")
                    addOption("-o", outputTemplate)
                }

                YoutubeDL.getInstance().execute(request)

                val infoFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".info.json") }
                    ?: return@withContext Result.failure(
                        IllegalStateException("Could not extract video metadata. Check the URL or update yt-dlp in Settings.")
                    )

                onProgress(0.42f, "Parsing replay heatmap & chapter cues...")
                val infoJson = JSONObject(infoFile.readText(Charsets.UTF_8))
                val videoTitle = infoJson.optString("title").ifBlank { "Untitled Stream / Video" }
                val channelName = infoJson.optString("uploader")
                    .ifBlank { infoJson.optString("channel").ifBlank { "Creator" } }
                val durationSec = infoJson.optDouble("duration", 0.0).coerceAtLeast(1.0)

                val heatmap = parseHeatmapFromInfoJson(infoJson)
                val rawCandidates = mutableListOf<ClipCandidate>()

                // 1. Most Replayed (Heatmap) Detector
                if (heatmap.isNotEmpty()) {
                    rawCandidates.addAll(detectHeatmapPeaks(heatmap, durationSec))
                } else {
                    // Fallback chapter/timestamp detector for Facebook & non-heatmap videos
                    rawCandidates.addAll(detectChaptersAndDescriptionCues(infoJson, durationSec))
                }

                // 2. Streaming Super Chat + Chat Velocity Detector
                onProgress(0.58f, "Stream-scanning live chat & Super Chats (RAM-safe)...")
                val liveChatFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".live_chat.json") }
                var allSuperChats = emptyList<SuperChatEvent>()
                if (liveChatFile != null) {
                    val chatOutput = SubtitleAndChatParser.parseLiveChatStreaming(liveChatFile, durationSec)
                    allSuperChats = chatOutput.superChats

                    for (spike in chatOutput.velocitySpikes) {
                        rawCandidates.add(
                            ClipCandidate(
                                id = UUID.randomUUID().toString(),
                                title = "Chat Hype Surge (${spike.messageCount} msgs/10s)",
                                startSec = (spike.startSec - 4.0).coerceAtLeast(0.0),
                                endSec = (spike.endSec + 10.0).coerceAtMost(durationSec),
                                hypeScore = (70 + (spike.multiplierOverAvg * 6.0).toInt()).coerceIn(65, 96),
                                signals = listOf(SignalSource.CHAT_HYPE),
                                isMultiSignal = false,
                                reason = String.format(
                                    Locale.US,
                                    "Chat exploded to %.1fx average message rate",
                                    spike.multiplierOverAvg
                                )
                            )
                        )
                    }
                }

                // 3. Subtitle / Transcript Parser
                onProgress(0.70f, "Indexing spoken transcript cues...")
                val vttFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".vtt") }
                val cues = if (vttFile != null) {
                    SubtitleAndChatParser.parseVttSubtitles(vttFile)
                } else {
                    emptyList()
                }

                // Filter Super Chats by threshold & optionally align reaction with AI
                val filteredSuperChats = allSuperChats.filter { it.usdApprox >= superChatThreshold.minUsd }
                val alignedRanges = if (aiConfig.canUseAi() && filteredSuperChats.isNotEmpty() && cues.isNotEmpty()) {
                    onProgress(0.78f, "AI-aligning Super Chat donor reactions...")
                    aiClient.alignSuperChatReactions(aiConfig, filteredSuperChats, cues, durationSec)
                } else {
                    emptyMap()
                }

                for (sc in filteredSuperChats) {
                    val aligned = alignedRanges[sc.offsetSec]
                    val start = aligned?.first ?: (sc.offsetSec - 4.0).coerceAtLeast(0.0)
                    val end = aligned?.second ?: (sc.offsetSec + 22.0).coerceAtMost(durationSec)
                    val baseScore = when {
                        sc.usdApprox >= 50.0 -> 95
                        sc.usdApprox >= 25.0 -> 90
                        sc.usdApprox >= 10.0 -> 84
                        sc.usdApprox >= 5.0 -> 78
                        else -> 72
                    }
                    rawCandidates.add(
                        ClipCandidate(
                            id = UUID.randomUUID().toString(),
                            title = "${sc.donor} • ${sc.amountDisplay}",
                            startSec = start,
                            endSec = end,
                            hypeScore = baseScore,
                            signals = listOf(SignalSource.SUPER_CHAT),
                            isMultiSignal = false,
                            superChat = sc,
                            reason = if (aligned != null) {
                                "Super Chat aligned with streamer reaction"
                            } else {
                                "Paid Super Chat highlight (${sc.amountDisplay})"
                            }
                        )
                    )
                }

                // 4. AI Viral Picks & Custom Prompt Search
                if (aiConfig.canUseAi() && cues.isNotEmpty() &&
                    (mode == DetectionMode.SMART_ALL || mode == DetectionMode.AI_CUSTOM)
                ) {
                    onProgress(0.86f, "Running AI viral hook & prompt scan...")
                    val peakCenters = rawCandidates.map { (it.startSec + it.endSec) / 2.0 }
                    val aiSuggestions = aiClient.findViralAndCustomClips(
                        config = aiConfig,
                        videoTitle = videoTitle,
                        durationSec = durationSec,
                        cues = cues,
                        peakCentersSec = peakCenters,
                        customPrompt = if (mode == DetectionMode.AI_CUSTOM) customAiPrompt else ""
                    )
                    for (pick in aiSuggestions) {
                        rawCandidates.add(
                            ClipCandidate(
                                id = UUID.randomUUID().toString(),
                                title = pick.title,
                                startSec = pick.startSec,
                                endSec = pick.endSec,
                                hypeScore = pick.score,
                                signals = listOf(SignalSource.AI_PICK),
                                isMultiSignal = false,
                                reason = pick.reason
                            )
                        )
                    }
                }

                // 5. Filter by DetectionMode & run Multi-Signal Consensus Engine
                onProgress(0.95f, "Merging multi-signal consensus clips...")
                val modeFiltered = filterCandidatesByMode(rawCandidates, mode)
                val consensusClips = runMultiSignalConsensus(
                    candidates = modeFiltered,
                    cues = cues,
                    paddingPreset = paddingPreset,
                    durationSec = durationSec
                )

                val summary = buildString {
                    append("${consensusClips.size} clips found")
                    if (heatmap.isNotEmpty()) append(" • Heatmap")
                    if (allSuperChats.isNotEmpty()) append(" • ${allSuperChats.size} Super Chats")
                    if (cues.isNotEmpty()) append(" • Transcript")
                }

                onProgress(1.0f, "Analysis complete!")
                Result.success(
                    VideoAnalysisResult(
                        sourceUrlOrUri = rawUrl.trim(),
                        isLocalFile = false,
                        localFilePath = null,
                        videoTitle = videoTitle,
                        channelName = channelName,
                        durationSec = durationSec,
                        heatmap = heatmap,
                        clips = consensusClips,
                        hasLiveChat = liveChatFile != null,
                        hasTranscript = cues.isNotEmpty(),
                        analysisSummary = summary
                    )
                )
            } finally {
                workDir.deleteRecursively()
            }
        } catch (t: Throwable) {
            Result.failure(t)
        }
    }

    suspend fun analyzeLocalVideo(
        context: Context,
        uri: Uri,
        paddingPreset: PaddingPreset,
        onProgress: (Float, String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            onProgress(0.10f, "Initializing FFmpeg acoustic scanner...")
            EngineInitializer.ensureInitialized(context).getOrThrow()

            onProgress(0.25f, "Staging local video metadata...")
            val stagedFile = stageUriToCache(context, uri)
                ?: return@withContext Result.failure(IllegalStateException("Unable to read selected local video file."))

            val displayName = resolveDisplayName(context, uri) ?: stagedFile.nameWithoutExtension
            val durationSec = probeVideoDurationSec(stagedFile.absolutePath).coerceAtLeast(1.0)

            onProgress(0.50f, "Scanning audio RMS energy spikes with FFmpeg astats...")
            val request = FFmpegExecuteRequest(
                listOf(
                    "-hide_banner",
                    "-i", stagedFile.absolutePath,
                    "-af", "astats=metadata=1:reset=1",
                    "-f", "null",
                    "-"
                )
            )
            val response = FFmpeg.getInstance().execute(request)
            val logOutput = "${response.out}\n${response.err}"

            onProgress(0.82f, "Building acoustic energy curve & peak clips...")
            val (heatmap, rawPeaks) = parseAudioRmsPeaks(logOutput, durationSec)

            val consensusClips = runMultiSignalConsensus(
                candidates = rawPeaks,
                cues = emptyList(),
                paddingPreset = paddingPreset,
                durationSec = durationSec
            )

            onProgress(1.0f, "Local video analysis complete!")
            Result.success(
                VideoAnalysisResult(
                    sourceUrlOrUri = uri.toString(),
                    isLocalFile = true,
                    localFilePath = stagedFile.absolutePath,
                    videoTitle = displayName,
                    channelName = "Local Device Video",
                    durationSec = durationSec,
                    heatmap = heatmap,
                    clips = consensusClips,
                    hasLiveChat = false,
                    hasTranscript = false,
                    analysisSummary = "${consensusClips.size} audio energy peaks detected"
                )
            )
        } catch (t: Throwable) {
            Result.failure(t)
        }
    }

    private fun parseHeatmapFromInfoJson(infoJson: JSONObject): List<HeatmapPoint> {
        val arr = infoJson.optJSONArray("heatmap") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val obj = arr.optJSONObject(i) ?: continue
                val start = obj.optDouble("start_time", Double.NaN)
                val end = obj.optDouble("end_time", Double.NaN)
                val value = obj.optDouble("value", Double.NaN)
                if (!start.isNaN() && !end.isNaN() && !value.isNaN()) {
                    add(HeatmapPoint(start, end, value.coerceIn(0.0, 1.0)))
                }
            }
        }
    }

    private fun detectHeatmapPeaks(
        heatmap: List<HeatmapPoint>,
        durationSec: Double
    ): List<ClipCandidate> {
        if (heatmap.size < 3) return emptyList()
        val peaks = mutableListOf<ClipCandidate>()
        for (i in 1 until heatmap.lastIndex) {
            val prev = heatmap[i - 1].value
            val curr = heatmap[i].value
            val next = heatmap[i + 1].value
            if (curr >= 0.62 && curr >= prev && curr >= next) {
                val center = (heatmap[i].startSec + heatmap[i].endSec) / 2.0
                val start = (center - 12.0).coerceAtLeast(0.0)
                val end = (center + 18.0).coerceAtMost(durationSec)
                val score = (60 + (curr * 38.0).toInt()).coerceIn(60, 98)
                peaks.add(
                    ClipCandidate(
                        id = UUID.randomUUID().toString(),
                        title = "Most Replayed Spike (${(curr * 100.0).toInt()}%)",
                        startSec = start,
                        endSec = end,
                        hypeScore = score,
                        signals = listOf(SignalSource.HEATMAP),
                        isMultiSignal = false,
                        reason = "Viewer replay intensity hit ${(curr * 100.0).toInt()}% of peak"
                    )
                )
            }
        }
        return peaks.sortedByDescending { it.hypeScore }.take(12)
    }

    private fun detectChaptersAndDescriptionCues(
        infoJson: JSONObject,
        durationSec: Double
    ): List<ClipCandidate> {
        val results = mutableListOf<ClipCandidate>()
        val chapters = infoJson.optJSONArray("chapters")
        if (chapters != null && chapters.length() > 0) {
            for (i in 0 until chapters.length().coerceAtMost(12)) {
                val ch = chapters.optJSONObject(i) ?: continue
                val start = ch.optDouble("start_time", Double.NaN)
                val end = ch.optDouble("end_time", Double.NaN)
                val title = ch.optString("title").trim().ifBlank { "Chapter #${i + 1}" }
                if (!start.isNaN() && !end.isNaN() && end > start) {
                    val clippedEnd = minOf(end, start + 45.0).coerceAtMost(durationSec)
                    results.add(
                        ClipCandidate(
                            id = UUID.randomUUID().toString(),
                            title = title,
                            startSec = start.coerceAtLeast(0.0),
                            endSec = clippedEnd,
                            hypeScore = 74,
                            signals = listOf(SignalSource.HEATMAP),
                            isMultiSignal = false,
                            reason = "Chapter highlight marker"
                        )
                    )
                }
            }
            return results
        }

        val description = infoJson.optString("description")
        val tsRegex = Regex("""(?m)^(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\s+(.+)$""")
        val matches = tsRegex.findAll(description).toList().take(10)
        for (match in matches) {
            val h = match.groupValues[1].toDoubleOrNull() ?: 0.0
            val m = match.groupValues[2].toDoubleOrNull() ?: 0.0
            val s = match.groupValues[3].toDoubleOrNull() ?: 0.0
            val label = match.groupValues[4].trim().take(60)
            val start = (h * 3600.0 + m * 60.0 + s).coerceIn(0.0, (durationSec - 5.0).coerceAtLeast(0.0))
            val end = (start + 30.0).coerceAtMost(durationSec)
            results.add(
                ClipCandidate(
                    id = UUID.randomUUID().toString(),
                    title = label,
                    startSec = start,
                    endSec = end,
                    hypeScore = 72,
                    signals = listOf(SignalSource.HEATMAP),
                    isMultiSignal = false,
                    reason = "Timestamp highlight from video description"
                )
            )
        }
        return results
    }

    private fun parseAudioRmsPeaks(
        ffmpegStderr: String,
        durationSec: Double
    ): Pair<List<HeatmapPoint>, List<ClipCandidate>> {
        val ptsRegex = Regex("""pts_time:(\d+(?:\.\d+)?)""")
        val rmsRegex = Regex("""RMS level dB:\s*(-?\d+(?:\.\d+)?)""")

        val samples = mutableListOf<Pair<Double, Double>>()
        var latestPts = 0.0

        ffmpegStderr.lineSequence().forEach { line ->
            ptsRegex.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { pts ->
                latestPts = pts
            }
            rmsRegex.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { rmsDb ->
                if (rmsDb.isFinite() && rmsDb > -90.0) {
                    samples.add(latestPts to rmsDb)
                }
            }
        }

        if (samples.isEmpty()) {
            // Fallback evenly-spaced highlight markers if audio track is silent/missing
            val fallbackClip = ClipCandidate(
                id = UUID.randomUUID().toString(),
                title = "Opening Highlight",
                startSec = 0.0,
                endSec = minOf(25.0, durationSec),
                hypeScore = 70,
                signals = listOf(SignalSource.AUDIO_PEAK),
                isMultiSignal = false,
                reason = "Default opening segment"
            )
            return emptyList<HeatmapPoint>() to listOf(fallbackClip)
        }

        // Aggregate into 40 buckets for the Canvas Heatmap curve
        val bucketCount = 40
        val bucketSize = (durationSec / bucketCount.toDouble()).coerceAtLeast(1.0)
        val bucketMaxDb = DoubleArray(bucketCount) { -60.0 }

        for ((time, db) in samples) {
            val idx = (time / bucketSize).toInt().coerceIn(0, bucketCount - 1)
            if (db > bucketMaxDb[idx]) bucketMaxDb[idx] = db
        }

        val minDb = bucketMaxDb.minOrNull() ?: -60.0
        val maxDb = bucketMaxDb.maxOrNull() ?: -10.0
        val span = (maxDb - minDb).coerceAtLeast(1.0)

        val heatmap = (0 until bucketCount).map { idx ->
            val norm = ((bucketMaxDb[idx] - minDb) / span).coerceIn(0.05, 1.0)
            HeatmapPoint(
                startSec = idx * bucketSize,
                endSec = minOf((idx + 1) * bucketSize, durationSec),
                value = norm
            )
        }

        val meanDb = bucketMaxDb.average()
        val variance = bucketMaxDb.sumOf { (it - meanDb) * (it - meanDb) } / bucketCount.toDouble()
        val stdDb = sqrt(variance)
        val peakThresholdDb = meanDb + 1.15 * stdDb

        val peaks = mutableListOf<ClipCandidate>()
        for (idx in 0 until bucketCount) {
            val db = bucketMaxDb[idx]
            if (db >= peakThresholdDb) {
                val center = (idx + 0.5) * bucketSize
                val start = (center - 8.0).coerceAtLeast(0.0)
                val end = (center + 14.0).coerceAtMost(durationSec)
                val norm = ((db - minDb) / span).coerceIn(0.0, 1.0)
                val score = (68 + (norm * 29.0).toInt()).coerceIn(68, 97)
                peaks.add(
                    ClipCandidate(
                        id = UUID.randomUUID().toString(),
                        title = String.format(Locale.US, "Audio Energy Peak (%.1f dB)", db),
                        startSec = start,
                        endSec = end,
                        hypeScore = score,
                        signals = listOf(SignalSource.AUDIO_PEAK),
                        isMultiSignal = false,
                        reason = String.format(Locale.US, "Loudness surge %.1f dB above baseline", db - meanDb)
                    )
                )
            }
        }

        return heatmap to peaks.sortedByDescending { it.hypeScore }.take(12)
    }

    private fun filterCandidatesByMode(
        candidates: List<ClipCandidate>,
        mode: DetectionMode
    ): List<ClipCandidate> {
        return when (mode) {
            DetectionMode.SMART_ALL -> candidates
            DetectionMode.HEATMAP -> candidates.filter { SignalSource.HEATMAP in it.signals }
            DetectionMode.SUPER_CHAT -> candidates.filter { SignalSource.SUPER_CHAT in it.signals }
            DetectionMode.CHAT_HYPE -> candidates.filter { SignalSource.CHAT_HYPE in it.signals }
            DetectionMode.AUDIO_PEAKS -> candidates.filter { SignalSource.AUDIO_PEAK in it.signals }
            DetectionMode.AI_CUSTOM -> candidates.filter { SignalSource.AI_PICK in it.signals }
        }
    }

    private fun runMultiSignalConsensus(
        candidates: List<ClipCandidate>,
        cues: List<TranscriptCue>,
        paddingPreset: PaddingPreset,
        durationSec: Double
    ): List<ClipCandidate> {
        if (candidates.isEmpty()) return emptyList()

        val sorted = candidates.sortedBy { it.startSec }
        val mergedList = mutableListOf<ClipCandidate>()
        var current = sorted.first()

        for (i in 1 until sorted.size) {
            val next = sorted[i]
            // Merge overlapping or adjacent clips within 18 seconds
            if (next.startSec - current.endSec <= 18.0) {
                val combinedSignals = (current.signals + next.signals).distinct()
                val multiSignal = combinedSignals.size >= 2
                val baseMax = maxOf(current.hypeScore, next.hypeScore)
                val boostedScore = if (multiSignal) {
                    (baseMax + 11 * (combinedSignals.size - 1)).coerceIn(1, 100)
                } else {
                    baseMax
                }
                val preferredSuperChat = current.superChat ?: next.superChat
                val preferredTitle = when {
                    preferredSuperChat != null -> "${preferredSuperChat.donor} • ${preferredSuperChat.amountDisplay}"
                    next.hypeScore > current.hypeScore -> next.title
                    else -> current.title
                }
                val combinedReason = listOf(current.reason, next.reason)
                    .filter { it.isNotBlank() }
                    .distinct()
                    .joinToString(" + ")

                current = current.copy(
                    title = preferredTitle,
                    startSec = minOf(current.startSec, next.startSec),
                    endSec = maxOf(current.endSec, next.endSec),
                    hypeScore = boostedScore,
                    signals = combinedSignals,
                    isMultiSignal = multiSignal,
                    superChat = preferredSuperChat,
                    reason = combinedReason
                )
            } else {
                mergedList.add(finalizeClipWithPaddingAndQuote(current, cues, paddingPreset, durationSec))
                current = next
            }
        }
        mergedList.add(finalizeClipWithPaddingAndQuote(current, cues, paddingPreset, durationSec))

        return mergedList.sortedWith(
            compareByDescending<ClipCandidate> { it.isMultiSignal }
                .thenByDescending { it.hypeScore }
                .thenBy { it.startSec }
        )
    }

    private fun finalizeClipWithPaddingAndQuote(
        clip: ClipCandidate,
        cues: List<TranscriptCue>,
        paddingPreset: PaddingPreset,
        durationSec: Double
    ): ClipCandidate {
        val paddedStart = (clip.startSec - paddingPreset.beforeSec).coerceAtLeast(0.0)
        val paddedEnd = (clip.endSec + paddingPreset.afterSec)
            .coerceAtMost(durationSec)
            .coerceAtLeast((paddedStart + 3.0).coerceAtMost(durationSec))
        val quote = SubtitleAndChatParser.extractQuoteAround(cues, paddedStart, paddedEnd)
        return clip.copy(
            startSec = paddedStart,
            endSec = paddedEnd,
            transcriptQuote = quote
        )
    }

    private fun stageUriToCache(context: Context, uri: Uri): File? {
        return try {
            val localDir = File(context.cacheDir, "local_videos").apply { mkdirs() }
            localDir.listFiles()?.forEach { it.delete() }
            val fileName = resolveDisplayName(context, uri) ?: "local_input.mp4"
            val dest = File(localDir, fileName)
            context.contentResolver.openInputStream(uri)?.use { input ->
                FileOutputStream(dest).use { output ->
                    input.copyTo(output, bufferSize = 65536)
                }
            } ?: return null
            dest
        } catch (_: Throwable) {
            null
        }
    }

    private fun resolveDisplayName(context: Context, uri: Uri): String? {
        return try {
            context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                    if (idx >= 0) cursor.getString(idx) else null
                } else {
                    null
                }
            }
        } catch (_: Throwable) {
            null
        }
    }

    private fun probeVideoDurationSec(filePath: String): Double {
        val retriever = MediaMetadataRetriever()
        return try {
            retriever.setDataSource(filePath)
            val durationMs = retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull() ?: 0L
            durationMs / 1000.0
        } catch (_: Throwable) {
            0.0
        } finally {
            runCatching { retriever.release() }
        }
    }
}
""",
    )

    write_file(
        f"{base}/engine/ClipExporter.kt",
        """
package com.clippulse.studio.engine

import android.content.ContentValues
import android.content.Context
import android.media.MediaScannerConnection
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.ExportMode
import com.clippulse.studio.model.TimeFormatter
import com.yausername.ffmpeg.FFmpeg
import com.yausername.ffmpeg.FFmpegExecuteRequest
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.nio.charset.StandardCharsets
import java.util.Locale

object ClipExporter {

    fun exportSingleClip(
        context: Context,
        sourceUrlOrUri: String,
        isLocalFile: Boolean,
        localFilePath: String?,
        videoTitle: String,
        clip: ClipCandidate,
        clipIndex: Int,
        exportMode: ExportMode,
        includeTxtNotes: Boolean
    ): Result<String> {
        return try {
            EngineInitializer.ensureInitialized(context).getOrThrow()

            val workDir = File(context.cacheDir, "export_${System.currentTimeMillis()}_$clipIndex").apply {
                mkdirs()
            }

            try {
                val safeTitle = sanitizeFileName(clip.title).take(42).ifBlank { "Clip_${clipIndex + 1}" }
                val baseName = "ClipPulse_${clipIndex + 1}_$safeTitle"
                val rawCutFile = File(workDir, "raw_section.mp4")
                val finalMp4File = File(workDir, "$baseName.mp4")

                if (isLocalFile && !localFilePath.isNullOrBlank()) {
                    val startStr = TimeFormatter.formatFfmpegDuration(clip.startSec)
                    val durStr = TimeFormatter.formatFfmpegDuration(clip.durationSec)
                    val ffmpegArgs = if (exportMode == ExportMode.VERTICAL_CROP) {
                        listOf(
                            "-y",
                            "-ss", startStr,
                            "-i", localFilePath,
                            "-t", durStr,
                            "-vf", "crop=ih*9/16:ih",
                            "-c:v", "libx264",
                            "-preset", "veryfast",
                            "-crf", "21",
                            "-c:a", "aac",
                            "-b:a", "128k",
                            "-movflags", "+faststart",
                            finalMp4File.absolutePath
                        )
                    } else {
                        listOf(
                            "-y",
                            "-ss", startStr,
                            "-i", localFilePath,
                            "-t", durStr,
                            "-c", "copy",
                            "-movflags", "+faststart",
                            finalMp4File.absolutePath
                        )
                    }
                    FFmpeg.getInstance().execute(FFmpegExecuteRequest(ffmpegArgs))
                } else {
                    val startTs = TimeFormatter.formatSectionTimestamp(clip.startSec)
                    val endTs = TimeFormatter.formatSectionTimestamp(clip.endSec)
                    val sectionSpec = "*$startTs-$endTs"

                    val ytdlRequest = YoutubeDLRequest(sourceUrlOrUri).apply {
                        addOption(
                            "-f",
                            "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]/bv*[height<=1080]+ba/b[height<=1080]/best"
                        )
                        addOption("--merge-output-format", "mp4")
                        addOption("--download-sections", sectionSpec)
                        addOption("--force-keyframes-at-cuts")
                        addOption("--no-playlist")
                        addOption("-o", rawCutFile.absolutePath)
                    }
                    YoutubeDL.getInstance().execute(ytdlRequest)

                    val downloaded = workDir.listFiles()?.firstOrNull {
                        it.extension.equals("mp4", ignoreCase = true) || it.name.startsWith("raw_section")
                    } ?: throw IllegalStateException("Section download produced no output file.")

                    if (exportMode == ExportMode.VERTICAL_CROP) {
                        val cropArgs = listOf(
                            "-y",
                            "-i", downloaded.absolutePath,
                            "-vf", "crop=ih*9/16:ih",
                            "-c:v", "libx264",
                            "-preset", "veryfast",
                            "-crf", "21",
                            "-c:a", "aac",
                            "-b:a", "128k",
                            "-movflags", "+faststart",
                            finalMp4File.absolutePath
                        )
                        FFmpeg.getInstance().execute(FFmpegExecuteRequest(cropArgs))
                    } else {
                        val remuxArgs = listOf(
                            "-y",
                            "-i", downloaded.absolutePath,
                            "-c", "copy",
                            "-movflags", "+faststart",
                            finalMp4File.absolutePath
                        )
                        FFmpeg.getInstance().execute(FFmpegExecuteRequest(remuxArgs))
                    }
                }

                if (!finalMp4File.exists() || finalMp4File.length() == 0L) {
                    return Result.failure(IllegalStateException("Rendered MP4 is empty for ${clip.title}"))
                }

                val savedVideoLocation = saveMp4ToGallery(context, finalMp4File, "$baseName.mp4")
                if (includeTxtNotes) {
                    val notesContent = buildSidecarNotes(videoTitle, sourceUrlOrUri, clip, exportMode)
                    saveTxtToDocuments(context, "$baseName.txt", notesContent)
                }

                Result.success(savedVideoLocation)
            } finally {
                workDir.deleteRecursively()
            }
        } catch (t: Throwable) {
            Result.failure(t)
        }
    }

    private fun saveMp4ToGallery(context: Context, sourceMp4: File, displayName: String): String {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val resolver = context.contentResolver
            val values = ContentValues().apply {
                put(MediaStore.Video.Media.DISPLAY_NAME, displayName)
                put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
                put(MediaStore.Video.Media.RELATIVE_PATH, "${Environment.DIRECTORY_MOVIES}/ClipPulse")
                put(MediaStore.Video.Media.IS_PENDING, 1)
            }
            val itemUri = resolver.insert(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, values)
                ?: throw IllegalStateException("MediaStore failed to allocate gallery video URI.")

            resolver.openOutputStream(itemUri)?.use { out ->
                FileInputStream(sourceMp4).use { input ->
                    input.copyTo(out, bufferSize = 65536)
                }
            } ?: throw IllegalStateException("Unable to open gallery output stream.")

            values.clear()
            values.put(MediaStore.Video.Media.IS_PENDING, 0)
            resolver.update(itemUri, values, null, null)
            "Movies/ClipPulse/$displayName"
        } else {
            val moviesDir = File(
                Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES),
                "ClipPulse"
            ).apply { mkdirs() }
            val destFile = File(moviesDir, displayName)
            FileInputStream(sourceMp4).use { input ->
                FileOutputStream(destFile).use { out ->
                    input.copyTo(out, bufferSize = 65536)
                }
            }
            MediaScannerConnection.scanFile(context, arrayOf(destFile.absolutePath), arrayOf("video/mp4"), null)
            destFile.absolutePath
        }
    }

    private fun saveTxtToDocuments(context: Context, displayName: String, content: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val resolver = context.contentResolver
            val values = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, displayName)
                put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                put(MediaStore.MediaColumns.RELATIVE_PATH, "${Environment.DIRECTORY_DOCUMENTS}/ClipPulse")
                put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
            val uri = resolver.insert(MediaStore.Files.getContentUri("external"), values) ?: return
            resolver.openOutputStream(uri)?.use { out ->
                out.write(content.toByteArray(StandardCharsets.UTF_8))
            }
            values.clear()
            values.put(MediaStore.MediaColumns.IS_PENDING, 0)
            resolver.update(uri, values, null, null)
        } else {
            val docsDir = File(
                Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS),
                "ClipPulse"
            ).apply { mkdirs() }
            File(docsDir, displayName).writeText(content, StandardCharsets.UTF_8)
        }
    }

    private fun buildSidecarNotes(
        videoTitle: String,
        sourceUrlOrUri: String,
        clip: ClipCandidate,
        exportMode: ExportMode
    ): String {
        return buildString {
            appendLine("ClipPulse Studio Export Notes")
            appendLine("==============================")
            appendLine("Clip Title : ${clip.title}")
            appendLine("Source     : $videoTitle")
            appendLine("URL / URI  : $sourceUrlOrUri")
            appendLine(
                String.format(
                    Locale.US,
                    "Range      : %s - %s (%.1fs)",
                    TimeFormatter.formatTimestamp(clip.startSec),
                    TimeFormatter.formatTimestamp(clip.endSec),
                    clip.durationSec
                )
            )
            appendLine("Hype Score : ${clip.hypeScore}/100")
            appendLine("Signals    : ${clip.signals.joinToString(", ") { it.label }}")
            appendLine("Format     : ${exportMode.label}")
            clip.superChat?.let { sc ->
                appendLine("Super Chat : ${sc.donor} (${sc.amountDisplay}) — ${sc.message}")
            }
            if (clip.reason.isNotBlank()) {
                appendLine("Rationale  : ${clip.reason}")
            }
            if (clip.transcriptQuote.isNotBlank()) {
                appendLine()
                appendLine("Transcript Quote:")
                appendLine("\"${clip.transcriptQuote}\"")
            }
        }
    }

    private fun sanitizeFileName(raw: String): String {
        return raw.replace(Regex("""[^a-zA-Z0-9._-]+"""), "_").trim('_')
    }
}
""",
    )

    write_file(
        f"{base}/service/ClipExportService.kt",
        """
package com.clippulse.studio.service

import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.app.ServiceCompat
import com.clippulse.studio.engine.ClipExporter
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.ExportJobState
import com.clippulse.studio.model.ExportMode
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

object ExportProgressBus {
    private val _state = MutableStateFlow<ExportJobState>(ExportJobState.Idle)
    val state: StateFlow<ExportJobState> = _state.asStateFlow()

    @Volatile
    var pendingClips: List<ClipCandidate> = emptyList()

    fun update(newState: ExportJobState) {
        _state.value = newState
    }

    fun reset() {
        _state.value = ExportJobState.Idle
    }
}

class ClipExportService : Service() {
    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private var activeJob: Job? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val sourceUrlOrUri = intent?.getStringExtra(EXTRA_SOURCE_URL).orEmpty()
        val isLocalFile = intent?.getBooleanExtra(EXTRA_IS_LOCAL, false) ?: false
        val localFilePath = intent?.getStringExtra(EXTRA_LOCAL_PATH)
        val videoTitle = intent?.getStringExtra(EXTRA_VIDEO_TITLE).orEmpty()
        val exportModeName = intent?.getStringExtra(EXTRA_EXPORT_MODE) ?: ExportMode.FAST_COPY.name
        val includeTxt = intent?.getBooleanExtra(EXTRA_INCLUDE_TXT, true) ?: true
        val clips = ExportProgressBus.pendingClips

        val exportMode = runCatching { ExportMode.valueOf(exportModeName) }.getOrDefault(ExportMode.FAST_COPY)

        val initialNotif = buildNotification(
            title = "ClipPulse Exporting",
            text = "Preparing ${clips.size} clip(s)...",
            progress = 0,
            max = clips.size.coerceAtLeast(1),
            ongoing = true
        )
        ServiceCompat.startForeground(
            this,
            NOTIFICATION_ID,
            initialNotif,
            ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
        )

        if (clips.isEmpty() || sourceUrlOrUri.isBlank()) {
            ExportProgressBus.update(ExportJobState.Failed("No clips selected for export."))
            stopSelf()
            return START_NOT_STICKY
        }

        activeJob?.cancel()
        activeJob = serviceScope.launch {
            val savedLocations = mutableListOf<String>()
            var lastError: String? = null

            for ((index, clip) in clips.withIndex()) {
                val fraction = index.toFloat() / clips.size.toFloat()
                ExportProgressBus.update(
                    ExportJobState.Running(
                        currentIndex = index + 1,
                        total = clips.size,
                        currentTitle = clip.title,
                        progressFraction = fraction
                    )
                )
                notifyProgress(
                    title = "Exporting clip ${index + 1} of ${clips.size}",
                    text = clip.title,
                    progress = index,
                    max = clips.size,
                    ongoing = true
                )

                val result = ClipExporter.exportSingleClip(
                    context = applicationContext,
                    sourceUrlOrUri = sourceUrlOrUri,
                    isLocalFile = isLocalFile,
                    localFilePath = localFilePath,
                    videoTitle = videoTitle,
                    clip = clip,
                    clipIndex = index,
                    exportMode = exportMode,
                    includeTxtNotes = includeTxt
                )

                result.fold(
                    onSuccess = { location -> savedLocations.add(location) },
                    onFailure = { err -> lastError = err.message ?: "Export failed" }
                )
            }

            if (savedLocations.isNotEmpty()) {
                ExportProgressBus.update(
                    ExportJobState.Completed(
                        exportedCount = savedLocations.size,
                        savedLocations = savedLocations
                    )
                )
                notifyProgress(
                    title = "ClipPulse Export Complete",
                    text = "Saved ${savedLocations.size} clip(s) to Movies/ClipPulse",
                    progress = clips.size,
                    max = clips.size,
                    ongoing = false
                )
            } else {
                val errMsg = lastError ?: "Failed to export selected clips."
                ExportProgressBus.update(ExportJobState.Failed(errMsg))
                notifyProgress(
                    title = "ClipPulse Export Failed",
                    text = errMsg,
                    progress = 0,
                    max = 1,
                    ongoing = false
                )
            }

            stopForeground(STOP_FOREGROUND_DETACH)
            stopSelf()
        }

        return START_NOT_STICKY
    }

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    private fun buildNotification(
        title: String,
        text: String,
        progress: Int,
        max: Int,
        ongoing: Boolean
    ) = NotificationCompat.Builder(this, CHANNEL_ID)
        .setSmallIcon(android.R.drawable.stat_sys_download)
        .setContentTitle(title)
        .setContentText(text)
        .setOnlyAlertOnce(true)
        .setOngoing(ongoing)
        .apply {
            if (ongoing) {
                setProgress(max, progress, false)
            } else {
                setProgress(0, 0, false)
                setAutoCancel(true)
            }
        }
        .build()

    private fun notifyProgress(
        title: String,
        text: String,
        progress: Int,
        max: Int,
        ongoing: Boolean
    ) {
        try {
            val notif = buildNotification(title, text, progress, max, ongoing)
            NotificationManagerCompat.from(this).notify(
                if (ongoing) NOTIFICATION_ID else NOTIFICATION_ID + 1,
                notif
            )
        } catch (_: SecurityException) {
            // Notification permission not granted on Android 13+; export still completes cleanly.
        }
    }

    companion object {
        const val CHANNEL_ID = "clippulse_export_channel"
        const val NOTIFICATION_ID = 4102

        private const val EXTRA_SOURCE_URL = "extra_source_url"
        private const val EXTRA_IS_LOCAL = "extra_is_local"
        private const val EXTRA_LOCAL_PATH = "extra_local_path"
        private const val EXTRA_VIDEO_TITLE = "extra_video_title"
        private const val EXTRA_EXPORT_MODE = "extra_export_mode"
        private const val EXTRA_INCLUDE_TXT = "extra_include_txt"

        fun startExport(
            context: Context,
            sourceUrlOrUri: String,
            isLocalFile: Boolean,
            localFilePath: String?,
            videoTitle: String,
            clips: List<ClipCandidate>,
            exportMode: ExportMode,
            includeTxtNotes: Boolean
        ) {
            ExportProgressBus.pendingClips = clips
            val intent = Intent(context, ClipExportService::class.java).apply {
                putExtra(EXTRA_SOURCE_URL, sourceUrlOrUri)
                putExtra(EXTRA_IS_LOCAL, isLocalFile)
                putExtra(EXTRA_LOCAL_PATH, localFilePath)
                putExtra(EXTRA_VIDEO_TITLE, videoTitle)
                putExtra(EXTRA_EXPORT_MODE, exportMode.name)
                putExtra(EXTRA_INCLUDE_TXT, includeTxtNotes)
            }
            androidx.core.content.ContextCompat.startForegroundService(context, intent)
        }
    }
}
""",
    )

    write_file(
        f"{base}/viewmodel/ClipPulseViewModel.kt",
        """
package com.clippulse.studio.viewmodel

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.engine.EngineInitializer
import com.clippulse.studio.engine.VideoAnalysisEngine
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.AiPreset
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.ExportJobState
import com.clippulse.studio.model.ExportMode
import com.clippulse.studio.model.PaddingPreset
import com.clippulse.studio.model.SignalSource
import com.clippulse.studio.model.SuperChatThreshold
import com.clippulse.studio.model.VideoAnalysisResult
import com.clippulse.studio.network.UniversalAiClient
import com.clippulse.studio.service.ClipExportService
import com.clippulse.studio.service.ExportProgressBus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.math.abs

data class StudioUiState(
    val sourceInput: String = "",
    val detectionMode: DetectionMode = DetectionMode.SMART_ALL,
    val customAiPrompt: String = "",
    val superChatThreshold: SuperChatThreshold = SuperChatThreshold.ALL,
    val paddingPreset: PaddingPreset = PaddingPreset.BALANCED,
    val isAnalyzing: Boolean = false,
    val analysisProgress: Float = 0f,
    val analysisStatus: String = "",
    val analysisError: String? = null,
    val analysisResult: VideoAnalysisResult? = null,
    val activeSignalFilter: SignalSource? = null,
    val expandedClipId: String? = null,
    val focusedClipId: String? = null,
    val exportMode: ExportMode = ExportMode.FAST_COPY,
    val includeTxtNotes: Boolean = true,
    val aiConfig: AiConfig = AiConfig(),
    val aiConnectionState: AiConnectionState = AiConnectionState.Idle,
    val isFetchingModels: Boolean = false,
    val modelFetchError: String? = null,
    val isAiSheetOpen: Boolean = false,
    val isUpdatingYtDlp: Boolean = false,
    val ytDlpUpdateStatus: String? = null
)

class ClipPulseViewModel(application: Application) : AndroidViewModel(application) {
    private val configStore = AiConfigStore(application)
    private val aiClient = UniversalAiClient()
    private val analysisEngine = VideoAnalysisEngine(aiClient)

    private val _uiState = MutableStateFlow(
        StudioUiState(aiConfig = configStore.load())
    )
    val uiState: StateFlow<StudioUiState> = _uiState.asStateFlow()

    val exportState: StateFlow<ExportJobState> = ExportProgressBus.state

    fun updateSourceInput(value: String) {
        _uiState.update { it.copy(sourceInput = value, analysisError = null) }
    }

    fun onSharedUrlReceived(url: String) {
        _uiState.update { it.copy(sourceInput = url, analysisError = null) }
    }

    fun setDetectionMode(mode: DetectionMode) {
        _uiState.update { it.copy(detectionMode = mode) }
    }

    fun setCustomAiPrompt(prompt: String) {
        _uiState.update { it.copy(customAiPrompt = prompt) }
    }

    fun setSuperChatThreshold(threshold: SuperChatThreshold) {
        _uiState.update { it.copy(superChatThreshold = threshold) }
    }

    fun setPaddingPreset(preset: PaddingPreset) {
        _uiState.update { it.copy(paddingPreset = preset) }
    }

    fun setSignalFilter(signal: SignalSource?) {
        _uiState.update { it.copy(activeSignalFilter = signal) }
    }

    fun toggleClipExpanded(clipId: String) {
        _uiState.update { state ->
            state.copy(expandedClipId = if (state.expandedClipId == clipId) null else clipId)
        }
    }

    fun focusClipAtTime(targetSeconds: Double) {
        val clips = _uiState.value.analysisResult?.clips ?: return
        if (clips.isEmpty()) return
        val nearest = clips.minByOrNull { clip ->
            val center = (clip.startSec + clip.endSec) / 2.0
            abs(center - targetSeconds)
        } ?: return
        _uiState.update {
            it.copy(
                focusedClipId = nearest.id,
                expandedClipId = nearest.id
            )
        }
    }

    fun toggleClipSelected(clipId: String) {
        _uiState.update { state ->
            val result = state.analysisResult ?: return@update state
            val updated = result.clips.map { clip ->
                if (clip.id == clipId) clip.copy(selected = !clip.selected) else clip
            }
            state.copy(analysisResult = result.copy(clips = updated))
        }
    }

    fun selectAllClips(selected: Boolean) {
        _uiState.update { state ->
            val result = state.analysisResult ?: return@update state
            val filter = state.activeSignalFilter
            val updated = result.clips.map { clip ->
                if (filter == null || filter in clip.signals) {
                    clip.copy(selected = selected)
                } else {
                    clip
                }
            }
            state.copy(analysisResult = result.copy(clips = updated))
        }
    }

    fun nudgeClipStart(clipId: String, deltaSec: Double) {
        _uiState.update { state ->
            val result = state.analysisResult ?: return@update state
            val updated = result.clips.map { clip ->
                if (clip.id == clipId) {
                    val newStart = (clip.startSec + deltaSec)
                        .coerceIn(0.0, (clip.endSec - 2.0).coerceAtLeast(0.0))
                    clip.copy(startSec = newStart)
                } else {
                    clip
                }
            }
            state.copy(analysisResult = result.copy(clips = updated))
        }
    }

    fun nudgeClipEnd(clipId: String, deltaSec: Double) {
        _uiState.update { state ->
            val result = state.analysisResult ?: return@update state
            val maxDur = result.durationSec.coerceAtLeast(1.0)
            val updated = result.clips.map { clip ->
                if (clip.id == clipId) {
                    val newEnd = (clip.endSec + deltaSec)
                        .coerceIn((clip.startSec + 2.0).coerceAtMost(maxDur), maxDur)
                    clip.copy(endSec = newEnd)
                } else {
                    clip
                }
            }
            state.copy(analysisResult = result.copy(clips = updated))
        }
    }

    fun setExportMode(mode: ExportMode) {
        _uiState.update { it.copy(exportMode = mode) }
    }

    fun toggleIncludeTxtNotes() {
        _uiState.update { it.copy(includeTxtNotes = !it.includeTxtNotes) }
    }

    fun analyzeRemoteUrl() {
        val url = _uiState.value.sourceInput.trim()
        if (url.isBlank()) {
            _uiState.update { it.copy(analysisError = "Paste a YouTube, YouTube Live VOD, or Facebook video link first.") }
            return
        }
        if (_uiState.value.isAnalyzing) return

        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    isAnalyzing = true,
                    analysisProgress = 0.05f,
                    analysisStatus = "Preparing zero-download scan...",
                    analysisError = null
                )
            }

            val snapshot = _uiState.value
            val result = analysisEngine.analyzeRemoteUrl(
                context = getApplication(),
                rawUrl = url,
                mode = snapshot.detectionMode,
                superChatThreshold = snapshot.superChatThreshold,
                paddingPreset = snapshot.paddingPreset,
                customAiPrompt = snapshot.customAiPrompt,
                aiConfig = snapshot.aiConfig,
                onProgress = { progress, status ->
                    _uiState.update { it.copy(analysisProgress = progress, analysisStatus = status) }
                }
            )

            result.fold(
                onSuccess = { analysis ->
                    _uiState.update {
                        it.copy(
                            isAnalyzing = false,
                            analysisProgress = 1f,
                            analysisStatus = analysis.analysisSummary,
                            analysisResult = analysis,
                            activeSignalFilter = null,
                            expandedClipId = analysis.clips.firstOrNull()?.id,
                            focusedClipId = analysis.clips.firstOrNull()?.id
                        )
                    }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isAnalyzing = false,
                            analysisError = error.message ?: "Analysis failed."
                        )
                    }
                }
            )
        }
    }

    fun analyzeLocalVideoUri(uri: Uri) {
        if (_uiState.value.isAnalyzing) return
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    sourceInput = uri.toString(),
                    isAnalyzing = true,
                    analysisProgress = 0.05f,
                    analysisStatus = "Loading local video...",
                    analysisError = null
                )
            }

            val result = analysisEngine.analyzeLocalVideo(
                context = getApplication(),
                uri = uri,
                paddingPreset = _uiState.value.paddingPreset,
                onProgress = { progress, status ->
                    _uiState.update { it.copy(analysisProgress = progress, analysisStatus = status) }
                }
            )

            result.fold(
                onSuccess = { analysis ->
                    _uiState.update {
                        it.copy(
                            isAnalyzing = false,
                            analysisProgress = 1f,
                            analysisStatus = analysis.analysisSummary,
                            analysisResult = analysis,
                            activeSignalFilter = null,
                            expandedClipId = analysis.clips.firstOrNull()?.id,
                            focusedClipId = analysis.clips.firstOrNull()?.id
                        )
                    }
                },
                onFailure = { error ->
                    _uiState.update {
                        it.copy(
                            isAnalyzing = false,
                            analysisError = error.message ?: "Local video scan failed."
                        )
                    }
                }
            )
        }
    }

    fun exportSelectedClips() {
        val state = _uiState.value
        val result = state.analysisResult ?: return
        val selectedClips = result.clips.filter { it.selected }
        if (selectedClips.isEmpty()) return

        ClipExportService.startExport(
            context = getApplication(),
            sourceUrlOrUri = result.sourceUrlOrUri,
            isLocalFile = result.isLocalFile,
            localFilePath = result.localFilePath,
            videoTitle = result.videoTitle,
            clips = selectedClips,
            exportMode = state.exportMode,
            includeTxtNotes = state.includeTxtNotes
        )
    }

    fun dismissExportStatus() {
        ExportProgressBus.reset()
    }

    // --- Universal AI API Manager Controls ---

    fun setAiSheetOpen(open: Boolean) {
        _uiState.update { it.copy(isAiSheetOpen = open) }
    }

    fun selectAiPreset(preset: AiPreset) {
        updateAndPersistAiConfig { current ->
            current.copy(
                preset = preset,
                baseUrl = preset.defaultBaseUrl,
                selectedModel = preset.defaultModel
            )
        }
    }

    fun updateAiBaseUrl(url: String) {
        updateAndPersistAiConfig { it.copy(baseUrl = url) }
    }

    fun updatePrimaryApiKey(key: String) {
        updateAndPersistAiConfig { it.copy(primaryKey = key) }
    }

    fun addBackupApiKey(key: String) {
        val clean = key.trim()
        if (clean.isBlank()) return
        updateAndPersistAiConfig { current ->
            current.copy(backupKeys = (current.backupKeys + clean).distinct())
        }
    }

    fun removeBackupApiKey(key: String) {
        updateAndPersistAiConfig { current ->
            current.copy(backupKeys = current.backupKeys.filterNot { it == key })
        }
    }

    fun selectAiModel(model: String) {
        updateAndPersistAiConfig { it.copy(selectedModel = model) }
    }

    fun setSmartPeakOnly(enabled: Boolean) {
        updateAndPersistAiConfig { it.copy(smartPeakOnly = enabled) }
    }

    fun setOfflineNoAiMode(enabled: Boolean) {
        updateAndPersistAiConfig { it.copy(offlineNoAiMode = enabled) }
    }

    private fun updateAndPersistAiConfig(transform: (AiConfig) -> AiConfig) {
        _uiState.update { state ->
            val updated = transform(state.aiConfig)
            configStore.save(updated)
            state.copy(aiConfig = updated, modelFetchError = null)
        }
    }

    fun fetchAvailableModels() {
        val currentConfig = _uiState.value.aiConfig
        val normalized = currentConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(currentConfig.baseUrl))
        configStore.save(normalized)

        viewModelScope.launch {
            _uiState.update {
                it.copy(aiConfig = normalized, isFetchingModels = true, modelFetchError = null)
            }
            val result = aiClient.fetchModels(normalized)
            result.fold(
                onSuccess = { models ->
                    val chosen = if (normalized.selectedModel in models) {
                        normalized.selectedModel
                    } else {
                        models.first()
                    }
                    val updated = normalized.copy(
                        availableModels = models,
                        selectedModel = chosen
                    )
                    configStore.save(updated)
                    _uiState.update {
                        it.copy(
                            aiConfig = updated,
                            isFetchingModels = false,
                            modelFetchError = null
                        )
                    }
                },
                onFailure = { err ->
                    _uiState.update {
                        it.copy(
                            isFetchingModels = false,
                            modelFetchError = err.message ?: "Failed to fetch models"
                        )
                    }
                }
            )
        }
    }

    fun testAiConnection() {
        val currentConfig = _uiState.value.aiConfig
        val normalized = currentConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(currentConfig.baseUrl))
        configStore.save(normalized)

        viewModelScope.launch {
            _uiState.update {
                it.copy(aiConfig = normalized, aiConnectionState = AiConnectionState.Testing)
            }
            val connState = aiClient.testConnection(normalized)
            _uiState.update { it.copy(aiConnectionState = connState) }
        }
    }

    fun updateYtDlpBinary() {
        if (_uiState.value.isUpdatingYtDlp) return
        viewModelScope.launch(Dispatchers.IO) {
            _uiState.update { it.copy(isUpdatingYtDlp = true, ytDlpUpdateStatus = "Updating yt-dlp...") }
            val result = EngineInitializer.updateYtDlpEngine(getApplication())
            result.fold(
                onSuccess = { status ->
                    _uiState.update {
                        it.copy(isUpdatingYtDlp = false, ytDlpUpdateStatus = "yt-dlp status: $status")
                    }
                },
                onFailure = { err ->
                    _uiState.update {
                        it.copy(
                            isUpdatingYtDlp = false,
                            ytDlpUpdateStatus = "Update failed: ${err.message ?: "Unknown error"}"
                        )
                    }
                }
            )
        }
    }
}
""",
    )

    write_file(
        f"{base}/ui/theme/Theme.kt",
        """
package com.clippulse.studio.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val ObsidianBg = Color(0xFF0B0B0F)
val MatteSlate = Color(0xFF16161D)
val ElevatedSlate = Color(0xFF1F1F29)
val HairlineBorder = Color(0xFF262633)
val ElectricIndigo = Color(0xFF6366F1)
val ElectricIndigoLight = Color(0xFF818CF8)

val ColorGold = Color(0xFFF59E0B)
val ColorCrimson = Color(0xFFEF4444)
val ColorPurple = Color(0xFFA855F7)
val ColorCyan = Color(0xFF06B6D4)
val ColorEmerald = Color(0xFF10B981)

val TextPrimary = Color(0xFFF4F4F8)
val TextSecondary = Color(0xFF9CA3AF)
val TextMuted = Color(0xFF6B7280)

private val ClipPulseColorScheme = darkColorScheme(
    primary = ElectricIndigo,
    onPrimary = Color.White,
    primaryContainer = Color(0xFF282A5E),
    onPrimaryContainer = Color(0xFFE0E7FF),
    secondary = ColorCyan,
    onSecondary = ObsidianBg,
    tertiary = ColorGold,
    background = ObsidianBg,
    onBackground = TextPrimary,
    surface = MatteSlate,
    onSurface = TextPrimary,
    surfaceVariant = ElevatedSlate,
    onSurfaceVariant = TextSecondary,
    outline = HairlineBorder,
    outlineVariant = HairlineBorder,
    error = ColorCrimson,
    onError = Color.White
)

@Composable
fun ClipPulseTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = ClipPulseColorScheme,
        content = content
    )
}
""",
    )

    write_file(
        f"{base}/ui/components/ClipPulseLogo.kt",
        """
package com.clippulse.studio.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import com.clippulse.studio.ui.theme.ColorCyan
import com.clippulse.studio.ui.theme.ColorGold
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.MatteSlate

@Composable
fun ClipPulseLogo(modifier: Modifier = Modifier.size(34.dp)) {
    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height

        drawRoundRect(
            color = MatteSlate,
            size = Size(w, h),
            cornerRadius = CornerRadius(w * 0.24f, h * 0.24f)
        )

        drawRoundRect(
            brush = Brush.linearGradient(listOf(ElectricIndigo, ColorCyan)),
            size = Size(w, h),
            cornerRadius = CornerRadius(w * 0.24f, h * 0.24f),
            style = Stroke(width = w * 0.06f)
        )

        val pulsePath = Path().apply {
            moveTo(w * 0.16f, h * 0.54f)
            lineTo(w * 0.30f, h * 0.54f)
            lineTo(w * 0.39f, h * 0.28f)
            lineTo(w * 0.50f, h * 0.76f)
            lineTo(w * 0.61f, h * 0.34f)
            lineTo(w * 0.70f, h * 0.58f)
            lineTo(w * 0.84f, h * 0.54f)
        }

        drawPath(
            path = pulsePath,
            brush = Brush.horizontalGradient(listOf(ElectricIndigo, ColorCyan)),
            style = Stroke(
                width = w * 0.085f,
                cap = StrokeCap.Round,
                join = StrokeJoin.Round
            )
        )

        drawCircle(
            color = ColorGold,
            radius = w * 0.08f,
            center = Offset(w * 0.78f, h * 0.24f)
        )
    }
}
""",
    )

    write_file(
        f"{base}/ui/components/InteractiveHeatmapTimeline.kt",
        """
package com.clippulse.studio.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.HeatmapPoint
import com.clippulse.studio.model.TimeFormatter
import com.clippulse.studio.ui.theme.ColorCrimson
import com.clippulse.studio.ui.theme.ColorGold
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.MatteSlate
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary

@Composable
fun InteractiveHeatmapTimeline(
    durationSec: Double,
    heatmap: List<HeatmapPoint>,
    clips: List<ClipCandidate>,
    focusedClipId: String?,
    onJumpToTime: (Double) -> Unit,
    modifier: Modifier = Modifier
) {
    val safeDuration = durationSec.coerceAtLeast(1.0)

    Surface(
        modifier = modifier.fillMaxWidth(),
        color = MatteSlate,
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(1.dp, HairlineBorder)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "REPLAY HEATMAP & SIGNAL TIMELINE",
                    color = TextSecondary,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.SemiBold,
                    letterSpacing = 0.8.sp
                )
                Text(
                    text = "Tap curve to jump",
                    color = TextMuted,
                    fontSize = 11.sp
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(86.dp)
                    .pointerInput(safeDuration, clips) {
                        detectTapGestures { offset ->
                            val ratio = (offset.x / size.width.toFloat()).coerceIn(0f, 1f)
                            onJumpToTime(ratio * safeDuration)
                        }
                    }
                    .pointerInput(safeDuration, clips) {
                        detectHorizontalDragGestures { change, _ ->
                            val ratio = (change.position.x / size.width.toFloat()).coerceIn(0f, 1f)
                            onJumpToTime(ratio * safeDuration)
                        }
                    }
            ) {
                val w = size.width
                val h = size.height

                // Base track background
                drawRoundRect(
                    color = ElevatedSlate,
                    size = Size(w, h)
                )

                // Horizontal guide lines
                for (row in 1..2) {
                    val y = h * (row / 3f)
                    drawLine(
                        color = HairlineBorder,
                        start = Offset(0f, y),
                        end = Offset(w, y),
                        strokeWidth = 1.dp.toPx()
                    )
                }

                // Plot heatmap gradient curve
                if (heatmap.size >= 2) {
                    val linePath = Path()
                    val fillPath = Path()

                    heatmap.forEachIndexed { idx, point ->
                        val centerSec = (point.startSec + point.endSec) / 2.0
                        val x = ((centerSec / safeDuration).toFloat().coerceIn(0f, 1f)) * w
                        val y = h - (point.value.toFloat().coerceIn(0.05f, 1f) * (h * 0.82f)) - (h * 0.06f)

                        if (idx == 0) {
                            linePath.moveTo(0f, y)
                            fillPath.moveTo(0f, h)
                            fillPath.lineTo(0f, y)
                        }
                        linePath.lineTo(x, y)
                        fillPath.lineTo(x, y)

                        if (idx == heatmap.lastIndex) {
                            linePath.lineTo(w, y)
                            fillPath.lineTo(w, y)
                            fillPath.lineTo(w, h)
                            fillPath.close()
                        }
                    }

                    drawPath(
                        path = fillPath,
                        brush = Brush.verticalGradient(
                            colors = listOf(
                                ColorCrimson.copy(alpha = 0.34f),
                                ElectricIndigo.copy(alpha = 0.06f)
                            )
                        )
                    )

                    drawPath(
                        path = linePath,
                        brush = Brush.horizontalGradient(
                            colors = listOf(ElectricIndigo, ColorCrimson, ColorGold)
                        ),
                        style = Stroke(width = 2.2.dp.toPx(), cap = StrokeCap.Round)
                    )
                }

                // Plot clip range highlights and vertical markers
                for (clip in clips) {
                    val startX = ((clip.startSec / safeDuration).toFloat().coerceIn(0f, 1f)) * w
                    val endX = ((clip.endSec / safeDuration).toFloat().coerceIn(0f, 1f)) * w
                    val markerColor = if (clip.isMultiSignal) {
                        ColorGold
                    } else {
                        clip.signals.firstOrNull()?.badgeColor ?: ElectricIndigo
                    }
                    val isFocused = clip.id == focusedClipId

                    drawRect(
                        color = markerColor.copy(alpha = if (isFocused) 0.34f else 0.16f),
                        topLeft = Offset(startX, 0f),
                        size = Size((endX - startX).coerceAtLeast(3.dp.toPx()), h)
                    )

                    drawLine(
                        color = if (isFocused) TextPrimary else markerColor,
                        start = Offset(startX, 0f),
                        end = Offset(startX, h),
                        strokeWidth = if (isFocused) 2.5.dp.toPx() else 1.5.dp.toPx()
                    )
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "00:00",
                    color = TextMuted,
                    fontSize = 11.sp
                )
                Text(
                    text = TimeFormatter.formatTimestamp(safeDuration / 2.0),
                    color = TextMuted,
                    fontSize = 11.sp
                )
                Text(
                    text = TimeFormatter.formatTimestamp(safeDuration),
                    color = TextMuted,
                    fontSize = 11.sp
                )
            }
        }
    }
}
""",
    )

    write_file(
        f"{base}/ui/components/ClipPreviewPlayer.kt",
        """
package com.clippulse.studio.ui.components

import android.net.Uri
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Pause
import androidx.compose.material.icons.rounded.PlayArrow
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import com.clippulse.studio.model.TimeFormatter
import com.clippulse.studio.ui.theme.ElectricIndigoLight
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.TextSecondary
import java.io.File

@Composable
fun ClipPreviewPlayer(
    localFilePath: String,
    startSec: Double,
    endSec: Double,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    var isPlaying by remember { mutableStateOf(false) }

    val exoPlayer = remember(localFilePath) {
        ExoPlayer.Builder(context).build().apply {
            val uri = Uri.fromFile(File(localFilePath))
            setMediaItem(MediaItem.fromUri(uri))
            prepare()
            seekTo((startSec * 1000.0).toLong())
        }
    }

    LaunchedEffect(startSec) {
        exoPlayer.seekTo((startSec * 1000.0).toLong())
    }

    DisposableEffect(exoPlayer) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
        }
        exoPlayer.addListener(listener)
        onDispose {
            exoPlayer.removeListener(listener)
            exoPlayer.release()
        }
    }

    Surface(
        modifier = modifier.fillMaxWidth(),
        color = ElevatedSlate,
        shape = RoundedCornerShape(12.dp),
        border = BorderStroke(1.dp, HairlineBorder)
    ) {
        Column(modifier = Modifier.padding(8.dp)) {
            AndroidView(
                factory = { ctx ->
                    PlayerView(ctx).apply {
                        player = exoPlayer
                        useController = false
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(170.dp)
            )

            Spacer(modifier = Modifier.height(6.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(
                        onClick = {
                            if (exoPlayer.isPlaying) {
                                exoPlayer.pause()
                            } else {
                                if (exoPlayer.currentPosition >= (endSec * 1000.0).toLong()) {
                                    exoPlayer.seekTo((startSec * 1000.0).toLong())
                                }
                                exoPlayer.play()
                            }
                        },
                        modifier = Modifier.size(32.dp)
                    ) {
                        Icon(
                            imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                            contentDescription = "Play or pause preview",
                            tint = ElectricIndigoLight
                        )
                    }

                    Spacer(modifier = Modifier.width(4.dp))

                    IconButton(
                        onClick = {
                            exoPlayer.seekTo((startSec * 1000.0).toLong())
                            exoPlayer.play()
                        },
                        modifier = Modifier.size(32.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.Refresh,
                            contentDescription = "Replay clip start",
                            tint = TextSecondary
                        )
                    }
                }

                Text(
                    text = "Preview: ${TimeFormatter.formatTimestamp(startSec)} - ${TimeFormatter.formatTimestamp(endSec)}",
                    color = TextSecondary,
                    fontSize = 11.sp
                )
            }
        }
    }
}
""",
    )

    write_file(
        f"{base}/ui/components/ClipCard.kt",
        """
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
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
import androidx.compose.material.icons.rounded.ExpandLess
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material.icons.rounded.Paid
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.TimeFormatter
import com.clippulse.studio.ui.theme.ColorEmerald
import com.clippulse.studio.ui.theme.ColorGold
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElectricIndigoLight
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.MatteSlate
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary
import java.util.Locale

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ClipCard(
    clip: ClipCandidate,
    isExpanded: Boolean,
    isFocused: Boolean,
    localVideoPath: String?,
    onToggleSelect: () -> Unit,
    onToggleExpand: () -> Unit,
    onNudgeStart: (Double) -> Unit,
    onNudgeEnd: (Double) -> Unit,
    modifier: Modifier = Modifier
) {
    val borderColor = when {
        isFocused -> ElectricIndigo
        clip.isMultiSignal -> ColorGold.copy(alpha = 0.55f)
        clip.selected -> HairlineBorder
        else -> HairlineBorder.copy(alpha = 0.5f)
    }

    Surface(
        modifier = modifier.fillMaxWidth(),
        color = MatteSlate,
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(if (isFocused) 1.5.dp else 1.dp, borderColor)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onToggleExpand() },
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = clip.selected,
                    onCheckedChange = { onToggleSelect() },
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
                            SignalPillBadge(
                                label = "\uD83D\uDD25 Multi-Signal",
                                accentColor = ColorGold
                            )
                        }
                        for (signal in clip.signals) {
                            SignalPillBadge(
                                label = signal.label,
                                accentColor = signal.badgeColor
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

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = String.format(
                            Locale.US,
                            "%s - %s  •  %.1fs",
                            TimeFormatter.formatTimestamp(clip.startSec),
                            TimeFormatter.formatTimestamp(clip.endSec),
                            clip.durationSec
                        ),
                        color = ElectricIndigoLight,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }

                Spacer(modifier = Modifier.width(8.dp))

                Column(horizontalAlignment = Alignment.End) {
                    val hypeColor = when {
                        clip.hypeScore >= 88 -> ColorGold
                        clip.hypeScore >= 76 -> ColorEmerald
                        else -> ElectricIndigoLight
                    }
                    Surface(
                        color = hypeColor.copy(alpha = 0.16f),
                        shape = RoundedCornerShape(10.dp),
                        border = BorderStroke(1.dp, hypeColor.copy(alpha = 0.45f))
                    ) {
                        Column(
                            modifier = Modifier.padding(horizontal = 9.dp, vertical = 5.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "${clip.hypeScore}",
                                color = hypeColor,
                                fontSize = 15.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = "HYPE",
                                color = hypeColor,
                                fontSize = 9.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(4.dp))

                    Icon(
                        imageVector = if (isExpanded) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore,
                        contentDescription = "Expand clip controls",
                        tint = TextSecondary,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }

            // Super Chat Donor Highlight Card
            clip.superChat?.let { sc ->
                Spacer(modifier = Modifier.height(8.dp))
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = ColorGold.copy(alpha = 0.12f),
                    shape = RoundedCornerShape(10.dp),
                    border = BorderStroke(1.dp, ColorGold.copy(alpha = 0.4f))
                ) {
                    Row(
                        modifier = Modifier.padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.Paid,
                            contentDescription = "Super Chat",
                            tint = ColorGold,
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "${sc.donor} donated ${sc.amountDisplay}",
                                color = ColorGold,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                            if (sc.message.isNotBlank()) {
                                Text(
                                    text = sc.message,
                                    color = TextPrimary,
                                    fontSize = 12.sp
                                )
                            }
                        }
                    }
                }
            }

            // Transcript Quote
            if (clip.transcriptQuote.isNotBlank()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "\"${clip.transcriptQuote}\"",
                    color = TextSecondary,
                    fontSize = 12.sp,
                    fontStyle = FontStyle.Italic,
                    maxLines = if (isExpanded) 5 else 2,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // Expandable Precision Trim & Inline Media3 Preview
            AnimatedVisibility(visible = isExpanded) {
                Column(modifier = Modifier.padding(top = 10.dp)) {
                    HorizontalDivider(color = HairlineBorder)
                    Spacer(modifier = Modifier.height(10.dp))

                    if (clip.reason.isNotBlank()) {
                        Text(
                            text = "Signal Rationale: ${clip.reason}",
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                    }

                    if (!localVideoPath.isNullOrBlank()) {
                        ClipPreviewPlayer(
                            localFilePath = localVideoPath,
                            startSec = clip.startSec,
                            endSec = clip.endSec
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                    }

                    // Precision Trim Nudge Controls (-2s / +2s Start & End)
                    Surface(
                        modifier = Modifier.fillMaxWidth(),
                        color = ElevatedSlate,
                        shape = RoundedCornerShape(12.dp),
                        border = BorderStroke(1.dp, HairlineBorder)
                    ) {
                        Column(modifier = Modifier.padding(10.dp)) {
                            Text(
                                text = "PRECISION TRIM NUDGE",
                                color = TextMuted,
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 0.7.sp
                            )
                            Spacer(modifier = Modifier.height(8.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "Start: ${TimeFormatter.formatTimestamp(clip.startSec)}",
                                    color = TextPrimary,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Medium
                                )
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeChipButton(label = "-2s", onClick = { onNudgeStart(-2.0) })
                                    NudgeChipButton(label = "+2s", onClick = { onNudgeStart(2.0) })
                                }
                            }

                            Spacer(modifier = Modifier.height(6.dp))

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "End: ${TimeFormatter.formatTimestamp(clip.endSec)}",
                                    color = TextPrimary,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Medium
                                )
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeChipButton(label = "-2s", onClick = { onNudgeEnd(-2.0) })
                                    NudgeChipButton(label = "+2s", onClick = { onNudgeEnd(2.0) })
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SignalPillBadge(label: String, accentColor: Color) {
    Surface(
        color = accentColor.copy(alpha = 0.16f),
        shape = RoundedCornerShape(6.dp),
        border = BorderStroke(1.dp, accentColor.copy(alpha = 0.45f))
    ) {
        Text(
            text = label,
            color = accentColor,
            fontSize = 10.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp)
        )
    }
}

@Composable
private fun NudgeChipButton(label: String, onClick: () -> Unit) {
    OutlinedButton(
        onClick = onClick,
        shape = RoundedCornerShape(8.dp),
        border = BorderStroke(1.dp, HairlineBorder),
        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp),
        modifier = Modifier.height(28.dp)
    ) {
        Text(
            text = label,
            color = ElectricIndigoLight,
            fontSize = 11.sp,
            fontWeight = FontWeight.SemiBold
        )
    }
}
""",
    )

    write_file(
        f"{base}/ui/components/AiManagerSheet.kt",
        """
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Bolt
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.Delete
import androidx.compose.material.icons.rounded.ErrorOutline
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material.icons.rounded.Update
import androidx.compose.material.icons.rounded.Visibility
import androidx.compose.material.icons.rounded.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.AiPreset
import com.clippulse.studio.ui.theme.ColorCrimson
import com.clippulse.studio.ui.theme.ColorEmerald
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElectricIndigoLight
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.MatteSlate
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun AiManagerSheet(
    config: AiConfig,
    connectionState: AiConnectionState,
    isFetchingModels: Boolean,
    modelFetchError: String?,
    isUpdatingYtDlp: Boolean,
    ytDlpUpdateStatus: String?,
    onDismiss: () -> Unit,
    onSelectPreset: (AiPreset) -> Unit,
    onUpdateBaseUrl: (String) -> Unit,
    onUpdatePrimaryKey: (String) -> Unit,
    onAddBackupKey: (String) -> Unit,
    onRemoveBackupKey: (String) -> Unit,
    onSelectModel: (String) -> Unit,
    onFetchModels: () -> Unit,
    onTestConnect: () -> Unit,
    onToggleSmartPeakOnly: (Boolean) -> Unit,
    onToggleOfflineMode: (Boolean) -> Unit,
    onUpdateYtDlp: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showPrimaryKey by remember { mutableStateOf(false) }
    var newBackupKeyInput by remember { mutableStateOf("") }
    var modelDropdownExpanded by remember { mutableStateOf(false) }
    var modelSearchFilter by remember { mutableStateOf("") }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = MatteSlate,
        contentColor = TextPrimary
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 18.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                text = "Universal AI API & Engine Manager",
                color = TextPrimary,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )

            Text(
                text = "Connect any OpenAI-compatible endpoint with automatic multi-key failover, or run 100% offline.",
                color = TextSecondary,
                fontSize = 12.sp
            )

            // 1-Tap Provider Presets
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                AiPreset.entries.forEach { preset ->
                    FilterChip(
                        selected = config.preset == preset,
                        onClick = { onSelectPreset(preset) },
                        label = { Text(preset.displayName, fontSize = 12.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = ElectricIndigo,
                            selectedLabelColor = TextPrimary,
                            containerColor = ElevatedSlate,
                            labelColor = TextSecondary
                        )
                    )
                }
            }

            // Base URL Input + Normalized Preview
            OutlinedTextField(
                value = config.baseUrl,
                onValueChange = onUpdateBaseUrl,
                label = { Text("Base URL") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            Text(
                text = "Normalized endpoint: ${AiConfigStore.normalizeBaseUrl(config.baseUrl)}",
                color = TextMuted,
                fontSize = 11.sp
            )

            // Primary API Key Input
            OutlinedTextField(
                value = config.primaryKey,
                onValueChange = onUpdatePrimaryKey,
                label = { Text("Primary API Key") },
                singleLine = true,
                visualTransformation = if (showPrimaryKey) {
                    VisualTransformation.None
                } else {
                    PasswordVisualTransformation()
                },
                trailingIcon = {
                    IconButton(onClick = { showPrimaryKey = !showPrimaryKey }) {
                        Icon(
                            imageVector = if (showPrimaryKey) Icons.Rounded.VisibilityOff else Icons.Rounded.Visibility,
                            contentDescription = "Toggle API key visibility",
                            tint = TextSecondary
                        )
                    }
                },
                modifier = Modifier.fillMaxWidth()
            )

            // Backup Failover Keys
            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = ElevatedSlate,
                shape = RoundedCornerShape(12.dp),
                border = BorderStroke(1.dp, HairlineBorder)
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(
                        text = "BACKUP FAILOVER KEYS (${config.backupKeys.size})",
                        color = TextSecondary,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                    Text(
                        text = "Automatically rotates to next key on HTTP 401, 403, 429, or 5xx.",
                        color = TextMuted,
                        fontSize = 11.sp
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        OutlinedTextField(
                            value = newBackupKeyInput,
                            onValueChange = { newBackupKeyInput = it },
                            placeholder = { Text("Add backup sk-...", fontSize = 12.sp) },
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        IconButton(
                            onClick = {
                                onAddBackupKey(newBackupKeyInput)
                                newBackupKeyInput = ""
                            }
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.Add,
                                contentDescription = "Add backup key",
                                tint = ElectricIndigoLight
                            )
                        }
                    }

                    config.backupKeys.forEachIndexed { idx, key ->
                        Spacer(modifier = Modifier.height(6.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            val masked = if (key.length > 10) {
                                "${key.take(6)}••••${key.takeLast(4)}"
                            } else {
                                "••••••••"
                            }
                            Text(
                                text = "Backup #${idx + 1}: $masked",
                                color = TextPrimary,
                                fontSize = 12.sp
                            )
                            IconButton(
                                onClick = { onRemoveBackupKey(key) },
                                modifier = Modifier.size(28.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Rounded.Delete,
                                    contentDescription = "Remove backup key",
                                    tint = ColorCrimson,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                }
            }

            // Dynamic Model Dropdown + Fetch Models Button
            ExposedDropdownMenuBox(
                expanded = modelDropdownExpanded,
                onExpandedChange = { modelDropdownExpanded = !modelDropdownExpanded }
            ) {
                OutlinedTextField(
                    value = config.selectedModel,
                    onValueChange = {
                        onSelectModel(it)
                        modelSearchFilter = it
                    },
                    label = { Text("Model ID (Select or Type)") },
                    singleLine = true,
                    trailingIcon = {
                        ExposedDropdownMenuDefaults.TrailingIcon(expanded = modelDropdownExpanded)
                    },
                    modifier = Modifier
                        .menuAnchor()
                        .fillMaxWidth()
                )

                val filteredModels = config.availableModels.filter {
                    modelSearchFilter.isBlank() || it.contains(modelSearchFilter, ignoreCase = true)
                }

                ExposedDropdownMenu(
                    expanded = modelDropdownExpanded && filteredModels.isNotEmpty(),
                    onDismissRequest = { modelDropdownExpanded = false },
                    modifier = Modifier.heightIn(max = 220.dp)
                ) {
                    filteredModels.forEach { modelId ->
                        DropdownMenuItem(
                            text = { Text(modelId, fontSize = 13.sp) },
                            onClick = {
                                onSelectModel(modelId)
                                modelSearchFilter = ""
                                modelDropdownExpanded = false
                            }
                        )
                    }
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                OutlinedButton(
                    onClick = onFetchModels,
                    enabled = !isFetchingModels,
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    if (isFetchingModels) {
                        CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                    } else {
                        Icon(
                            imageVector = Icons.Rounded.Refresh,
                            contentDescription = "Fetch models",
                            modifier = Modifier.size(16.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Fetch Models", fontSize = 13.sp)
                }

                Button(
                    onClick = onTestConnect,
                    enabled = connectionState !is AiConnectionState.Testing,
                    colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                    shape = RoundedCornerShape(10.dp),
                    modifier = Modifier.weight(1f)
                ) {
                    if (connectionState is AiConnectionState.Testing) {
                        CircularProgressIndicator(
                            color = TextPrimary,
                            modifier = Modifier.size(16.dp),
                            strokeWidth = 2.dp
                        )
                    } else {
                        Icon(
                            imageVector = Icons.Rounded.Bolt,
                            contentDescription = "Connect",
                            modifier = Modifier.size(16.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Connect", fontSize = 13.sp)
                }
            }

            if (modelFetchError != null) {
                Text(
                    text = modelFetchError,
                    color = ColorCrimson,
                    fontSize = 12.sp
                )
            }

            when (connectionState) {
                is AiConnectionState.Connected -> {
                    Surface(
                        color = ColorEmerald.copy(alpha = 0.14f),
                        shape = RoundedCornerShape(10.dp),
                        border = BorderStroke(1.dp, ColorEmerald.copy(alpha = 0.45f)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(10.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.CheckCircle,
                                contentDescription = "Connected",
                                tint = ColorEmerald,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "\u2713 Connected (${connectionState.latencyMs} ms) • ${connectionState.model}",
                                color = ColorEmerald,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                    }
                }
                is AiConnectionState.Error -> {
                    Surface(
                        color = ColorCrimson.copy(alpha = 0.14f),
                        shape = RoundedCornerShape(10.dp),
                        border = BorderStroke(1.dp, ColorCrimson.copy(alpha = 0.45f)),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(10.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.ErrorOutline,
                                contentDescription = "Connection Error",
                                tint = ColorCrimson,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = connectionState.message,
                                color = ColorCrimson,
                                fontSize = 12.sp
                            )
                        }
                    }
                }
                else -> Unit
            }

            HorizontalDivider(color = HairlineBorder)

            // Token Optimization & Offline Toggles
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Smart Peak-Only Mode (~85% token savings)",
                        color = TextPrimary,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        text = "Slices only 2-minute caption windows around peaks & Super Chats.",
                        color = TextMuted,
                        fontSize = 11.sp
                    )
                }
                Switch(
                    checked = config.smartPeakOnly,
                    onCheckedChange = onToggleSmartPeakOnly,
                    colors = SwitchDefaults.colors(checkedTrackColor = ElectricIndigo)
                )
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "100% Offline / No-AI Mode",
                        color = TextPrimary,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        text = "Runs Heatmap, Super Chat, Chat Hype & Audio Peak scanners with zero API keys.",
                        color = TextMuted,
                        fontSize = 11.sp
                    )
                }
                Switch(
                    checked = config.offlineNoAiMode,
                    onCheckedChange = onToggleOfflineMode,
                    colors = SwitchDefaults.colors(checkedTrackColor = ElectricIndigo)
                )
            }

            HorizontalDivider(color = HairlineBorder)

            // 1-Tap yt-dlp Engine Updater
            OutlinedButton(
                onClick = onUpdateYtDlp,
                enabled = !isUpdatingYtDlp,
                shape = RoundedCornerShape(10.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                if (isUpdatingYtDlp) {
                    CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                } else {
                    Icon(
                        imageVector = Icons.Rounded.Update,
                        contentDescription = "Update yt-dlp engine",
                        modifier = Modifier.size(16.dp)
                    )
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text("Update yt-dlp Extractor Engine (Zero APK Rebuild)", fontSize = 12.sp)
            }

            if (ytDlpUpdateStatus != null) {
                Text(
                    text = ytDlpUpdateStatus,
                    color = ElectricIndigoLight,
                    fontSize = 12.sp
                )
            }

            Spacer(modifier = Modifier.height(18.dp))
        }
    }
}
""",
    )

    write_file(
        f"{base}/ui/ClipPulseStudioScreen.kt",
        """
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui

import android.Manifest
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoAwesome
import androidx.compose.material.icons.rounded.ContentCut
import androidx.compose.material.icons.rounded.ContentPaste
import androidx.compose.material.icons.rounded.CropPortrait
import androidx.compose.material.icons.rounded.Description
import androidx.compose.material.icons.rounded.FileDownload
import androidx.compose.material.icons.rounded.VideoLibrary
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.clippulse.studio.model.AiConnectionState
import com.clippulse.studio.model.DetectionMode
import com.clippulse.studio.model.ExportJobState
import com.clippulse.studio.model.ExportMode
import com.clippulse.studio.model.PaddingPreset
import com.clippulse.studio.model.SignalSource
import com.clippulse.studio.model.SuperChatThreshold
import com.clippulse.studio.ui.components.AiManagerSheet
import com.clippulse.studio.ui.components.ClipCard
import com.clippulse.studio.ui.components.ClipPulseLogo
import com.clippulse.studio.ui.components.InteractiveHeatmapTimeline
import com.clippulse.studio.ui.theme.ColorCrimson
import com.clippulse.studio.ui.theme.ColorEmerald
import com.clippulse.studio.ui.theme.ColorGold
import com.clippulse.studio.ui.theme.ElectricIndigo
import com.clippulse.studio.ui.theme.ElectricIndigoLight
import com.clippulse.studio.ui.theme.ElevatedSlate
import com.clippulse.studio.ui.theme.HairlineBorder
import com.clippulse.studio.ui.theme.MatteSlate
import com.clippulse.studio.ui.theme.ObsidianBg
import com.clippulse.studio.ui.theme.TextMuted
import com.clippulse.studio.ui.theme.TextPrimary
import com.clippulse.studio.ui.theme.TextSecondary
import com.clippulse.studio.viewmodel.ClipPulseViewModel

@Composable
fun ClipPulseStudioScreen(viewModel: ClipPulseViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val exportState by viewModel.exportState.collectAsStateWithLifecycle()
    val clipboardManager = LocalClipboardManager.current

    val localVideoPicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            viewModel.analyzeLocalVideoUri(uri)
        }
    }

    val notificationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) {
        viewModel.exportSelectedClips()
    }

    val analysisResult = state.analysisResult
    val visibleClips = analysisResult?.clips?.filter { clip ->
        state.activeSignalFilter == null || state.activeSignalFilter in clip.signals
    }.orEmpty()
    val selectedCount = analysisResult?.clips?.count { it.selected } ?: 0

    Scaffold(
        containerColor = ObsidianBg,
        topBar = {
            StudioTopBar(
                aiConfig = state.aiConfig,
                connectionState = state.aiConnectionState,
                onOpenAiManager = { viewModel.setAiSheetOpen(true) }
            )
        },
        bottomBar = {
            if (analysisResult != null) {
                StickyExportDock(
                    selectedCount = selectedCount,
                    exportMode = state.exportMode,
                    includeTxtNotes = state.includeTxtNotes,
                    exportState = exportState,
                    onSelectExportMode = viewModel::setExportMode,
                    onToggleTxtNotes = viewModel::toggleIncludeTxtNotes,
                    onDismissExportState = viewModel::dismissExportStatus,
                    onExportClick = {
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                        } else {
                            viewModel.exportSelectedClips()
                        }
                    }
                )
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Source Input & Detection Controls Card
            item {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MatteSlate,
                    shape = RoundedCornerShape(18.dp),
                    border = BorderStroke(1.dp, HairlineBorder)
                ) {
                    Column(
                        modifier = Modifier.padding(14.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        Text(
                            text = "ZERO-DOWNLOAD STREAM & VIDEO SOURCE",
                            color = TextSecondary,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold,
                            letterSpacing = 0.8.sp
                        )

                        OutlinedTextField(
                            value = state.sourceInput,
                            onValueChange = viewModel::updateSourceInput,
                            placeholder = {
                                Text(
                                    "YouTube URL, Live VOD, or Facebook Video...",
                                    fontSize = 13.sp,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis
                                )
                            },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth()
                        )

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedButton(
                                onClick = {
                                    val pasted = clipboardManager.getText()?.text?.trim().orEmpty()
                                    if (pasted.isNotEmpty()) {
                                        viewModel.updateSourceInput(pasted)
                                    }
                                },
                                shape = RoundedCornerShape(10.dp),
                                border = BorderStroke(1.dp, HairlineBorder),
                                modifier = Modifier.weight(1f)
                            ) {
                                Icon(
                                    imageVector = Icons.Rounded.ContentPaste,
                                    contentDescription = "Paste link",
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Paste Link", fontSize = 12.sp)
                            }

                            OutlinedButton(
                                onClick = { localVideoPicker.launch("video/*") },
                                shape = RoundedCornerShape(10.dp),
                                border = BorderStroke(1.dp, HairlineBorder),
                                modifier = Modifier.weight(1f)
                            ) {
                                Icon(
                                    imageVector = Icons.Rounded.VideoLibrary,
                                    contentDescription = "Pick local video",
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text("Local Video", fontSize = 12.sp)
                            }
                        }

                        // Horizontal Detection Mode Pills
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            DetectionMode.entries.forEach { mode ->
                                FilterChip(
                                    selected = state.detectionMode == mode,
                                    onClick = { viewModel.setDetectionMode(mode) },
                                    label = { Text(mode.label, fontSize = 11.sp) },
                                    colors = FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = ElectricIndigo,
                                        selectedLabelColor = TextPrimary,
                                        containerColor = ElevatedSlate,
                                        labelColor = TextSecondary
                                    )
                                )
                            }
                        }

                        // Optional Custom AI Prompt Box
                        if (state.detectionMode == DetectionMode.AI_CUSTOM || state.detectionMode == DetectionMode.SMART_ALL) {
                            OutlinedTextField(
                                value = state.customAiPrompt,
                                onValueChange = viewModel::setCustomAiPrompt,
                                placeholder = {
                                    Text(
                                        "Optional AI prompt (e.g., \"every rage moment or clutch play\")",
                                        fontSize = 12.sp
                                    )
                                },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth()
                            )
                        }

                        // Super Chat Minimum Threshold Chips
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "Super Chat:",
                                color = TextMuted,
                                fontSize = 11.sp
                            )
                            SuperChatThreshold.entries.forEach { threshold ->
                                FilterChip(
                                    selected = state.superChatThreshold == threshold,
                                    onClick = { viewModel.setSuperChatThreshold(threshold) },
                                    label = { Text(threshold.label, fontSize = 11.sp) },
                                    colors = FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = ColorGold.copy(alpha = 0.25f),
                                        selectedLabelColor = ColorGold,
                                        containerColor = ElevatedSlate,
                                        labelColor = TextSecondary
                                    )
                                )
                            }
                        }

                        // Start / End Padding Chips
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "Padding:",
                                color = TextMuted,
                                fontSize = 11.sp
                            )
                            PaddingPreset.entries.forEach { preset ->
                                FilterChip(
                                    selected = state.paddingPreset == preset,
                                    onClick = { viewModel.setPaddingPreset(preset) },
                                    label = { Text(preset.label, fontSize = 11.sp) },
                                    colors = FilterChipDefaults.filterChipColors(
                                        selectedContainerColor = ElectricIndigo.copy(alpha = 0.28f),
                                        selectedLabelColor = ElectricIndigoLight,
                                        containerColor = ElevatedSlate,
                                        labelColor = TextSecondary
                                    )
                                )
                            }
                        }

                        Button(
                            onClick = viewModel::analyzeRemoteUrl,
                            enabled = !state.isAnalyzing,
                            colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(46.dp)
                        ) {
                            if (state.isAnalyzing) {
                                CircularProgressIndicator(
                                    color = TextPrimary,
                                    modifier = Modifier.size(18.dp),
                                    strokeWidth = 2.dp
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("Scanning Stream Signals...", fontWeight = FontWeight.SemiBold)
                            } else {
                                Icon(
                                    imageVector = Icons.Rounded.AutoAwesome,
                                    contentDescription = "Analyze",
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("Analyze Video (Zero-Download)", fontWeight = FontWeight.SemiBold)
                            }
                        }

                        if (state.isAnalyzing) {
                            LinearProgressIndicator(
                                progress = { state.analysisProgress },
                                color = ElectricIndigo,
                                trackColor = ElevatedSlate,
                                modifier = Modifier.fillMaxWidth()
                            )
                            Text(
                                text = state.analysisStatus,
                                color = ElectricIndigoLight,
                                fontSize = 12.sp
                            )
                        }

                        if (state.analysisError != null) {
                            Text(
                                text = state.analysisError.orEmpty(),
                                color = ColorCrimson,
                                fontSize = 12.sp
                            )
                        }
                    }
                }
            }

            // Analysis Results: Video Header, Interactive Heatmap Timeline & Filter Controls
            if (analysisResult != null) {
                item {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Surface(
                            modifier = Modifier.fillMaxWidth(),
                            color = MatteSlate,
                            shape = RoundedCornerShape(14.dp),
                            border = BorderStroke(1.dp, HairlineBorder)
                        ) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(
                                    text = analysisResult.videoTitle,
                                    color = TextPrimary,
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold,
                                    maxLines = 2,
                                    overflow = TextOverflow.Ellipsis
                                )
                                Spacer(modifier = Modifier.height(3.dp))
                                Text(
                                    text = "${analysisResult.channelName}  •  ${analysisResult.analysisSummary}",
                                    color = TextSecondary,
                                    fontSize = 12.sp
                                )
                            }
                        }

                        InteractiveHeatmapTimeline(
                            durationSec = analysisResult.durationSec,
                            heatmap = analysisResult.heatmap,
                            clips = analysisResult.clips,
                            focusedClipId = state.focusedClipId,
                            onJumpToTime = viewModel::focusClipAtTime
                        )

                        // Signal Filter Chips + Select All / Clear
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            FilterChip(
                                selected = state.activeSignalFilter == null,
                                onClick = { viewModel.setSignalFilter(null) },
                                label = { Text("All (${analysisResult.clips.size})", fontSize = 11.sp) }
                            )
                            SignalSource.entries.forEach { signal ->
                                val count = analysisResult.clips.count { signal in it.signals }
                                if (count > 0) {
                                    FilterChip(
                                        selected = state.activeSignalFilter == signal,
                                        onClick = {
                                            viewModel.setSignalFilter(
                                                if (state.activeSignalFilter == signal) null else signal
                                            )
                                        },
                                        label = { Text("${signal.label} ($count)", fontSize = 11.sp) }
                                    )
                                }
                            }
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "DETECTED CLIPS ($selectedCount/${analysisResult.clips.size} selected)",
                                color = TextSecondary,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.SemiBold,
                                letterSpacing = 0.7.sp
                            )
                            Row {
                                TextButton(onClick = { viewModel.selectAllClips(true) }) {
                                    Text("Select All", color = ElectricIndigoLight, fontSize = 12.sp)
                                }
                                TextButton(onClick = { viewModel.selectAllClips(false) }) {
                                    Text("Clear", color = TextSecondary, fontSize = 12.sp)
                                }
                            }
                        }
                    }
                }

                items(
                    items = visibleClips,
                    key = { it.id }
                ) { clip ->
                    ClipCard(
                        clip = clip,
                        isExpanded = state.expandedClipId == clip.id,
                        isFocused = state.focusedClipId == clip.id,
                        localVideoPath = analysisResult.localFilePath,
                        onToggleSelect = { viewModel.toggleClipSelected(clip.id) },
                        onToggleExpand = { viewModel.toggleClipExpanded(clip.id) },
                        onNudgeStart = { delta -> viewModel.nudgeClipStart(clip.id, delta) },
                        onNudgeEnd = { delta -> viewModel.nudgeClipEnd(clip.id, delta) }
                    )
                }
            }
        }
    }

    if (state.isAiSheetOpen) {
        AiManagerSheet(
            config = state.aiConfig,
            connectionState = state.aiConnectionState,
            isFetchingModels = state.isFetchingModels,
            modelFetchError = state.modelFetchError,
            isUpdatingYtDlp = state.isUpdatingYtDlp,
            ytDlpUpdateStatus = state.ytDlpUpdateStatus,
            onDismiss = { viewModel.setAiSheetOpen(false) },
            onSelectPreset = viewModel::selectAiPreset,
            onUpdateBaseUrl = viewModel::updateAiBaseUrl,
            onUpdatePrimaryKey = viewModel::updatePrimaryApiKey,
            onAddBackupKey = viewModel::addBackupApiKey,
            onRemoveBackupKey = viewModel::removeBackupApiKey,
            onSelectModel = viewModel::selectAiModel,
            onFetchModels = viewModel::fetchAvailableModels,
            onTestConnect = viewModel::testAiConnection,
            onToggleSmartPeakOnly = viewModel::setSmartPeakOnly,
            onToggleOfflineMode = viewModel::setOfflineNoAiMode,
            onUpdateYtDlp = viewModel::updateYtDlpBinary
        )
    }
}

@Composable
private fun StudioTopBar(
    aiConfig: com.clippulse.studio.model.AiConfig,
    connectionState: AiConnectionState,
    onOpenAiManager: () -> Unit
) {
    Surface(
        color = ObsidianBg,
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                ClipPulseLogo()
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
                        fontSize = 11.sp
                    )
                }
            }

            // Top-right live AI status pill
            val (pillText, pillColor) = when {
                aiConfig.offlineNoAiMode -> "Offline Mode" to TextSecondary
                connectionState is AiConnectionState.Connected -> "\u2713 ${connectionState.latencyMs}ms" to ColorEmerald
                connectionState is AiConnectionState.Error -> "AI Error" to ColorCrimson
                aiConfig.primaryKey.isNotBlank() -> aiConfig.preset.displayName to ElectricIndigoLight
                else -> "Setup AI" to ColorGold
            }

            Surface(
                onClick = onOpenAiManager,
                color = pillColor.copy(alpha = 0.14f),
                shape = RoundedCornerShape(20.dp),
                border = BorderStroke(1.dp, pillColor.copy(alpha = 0.45f))
            ) {
                Text(
                    text = pillText,
                    color = pillColor,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                )
            }
        }
    }
}

@Composable
private fun StickyExportDock(
    selectedCount: Int,
    exportMode: ExportMode,
    includeTxtNotes: Boolean,
    exportState: ExportJobState,
    onSelectExportMode: (ExportMode) -> Unit,
    onToggleTxtNotes: () -> Unit,
    onDismissExportState: () -> Unit,
    onExportClick: () -> Unit
) {
    Surface(
        color = MatteSlate,
        border = BorderStroke(1.dp, HairlineBorder),
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
    ) {
        Column(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            when (exportState) {
                is ExportJobState.Running -> {
                    LinearProgressIndicator(
                        progress = { exportState.progressFraction },
                        color = ElectricIndigo,
                        trackColor = ElevatedSlate,
                        modifier = Modifier.fillMaxWidth()
                    )
                    Text(
                        text = "Exporting ${exportState.currentIndex}/${exportState.total}: ${exportState.currentTitle}",
                        color = ElectricIndigoLight,
                        fontSize = 12.sp,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                is ExportJobState.Completed -> {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Saved ${exportState.exportedCount} clip(s) to Movies/ClipPulse",
                            color = ColorEmerald,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        TextButton(onClick = onDismissExportState) {
                            Text("OK", color = ColorEmerald, fontSize = 12.sp)
                        }
                    }
                }
                is ExportJobState.Failed -> {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = exportState.error,
                            color = ColorCrimson,
                            fontSize = 12.sp,
                            modifier = Modifier.weight(1f)
                        )
                        TextButton(onClick = onDismissExportState) {
                            Text("Dismiss", color = ColorCrimson, fontSize = 12.sp)
                        }
                    }
                }
                ExportJobState.Idle -> Unit
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                FilterChip(
                    selected = exportMode == ExportMode.FAST_COPY,
                    onClick = { onSelectExportMode(ExportMode.FAST_COPY) },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Rounded.ContentCut,
                            contentDescription = "Fast Cut",
                            modifier = Modifier.size(14.dp)
                        )
                    },
                    label = { Text("Fast Cut", fontSize = 11.sp) }
                )

                FilterChip(
                    selected = exportMode == ExportMode.VERTICAL_CROP,
                    onClick = { onSelectExportMode(ExportMode.VERTICAL_CROP) },
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Rounded.CropPortrait,
                            contentDescription = "9:16 Crop",
                            modifier = Modifier.size(14.dp)
                        )
                    },
                    label = { Text("9:16 Crop", fontSize = 11.sp) }
                )

                FilterChip(
                    selected = includeTxtNotes,
                    onClick = onToggleTxtNotes,
                    leadingIcon = {
                        Icon(
                            imageVector = Icons.Rounded.Description,
                            contentDescription = "Include TXT sidecar notes",
                            modifier = Modifier.size(14.dp)
                        )
                    },
                    label = { Text("+.TXT", fontSize = 11.sp) }
                )
            }

            Button(
                onClick = onExportClick,
                enabled = selectedCount > 0 && exportState !is ExportJobState.Running,
                colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo),
                shape = RoundedCornerShape(12.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(46.dp)
            ) {
                Icon(
                    imageVector = Icons.Rounded.FileDownload,
                    contentDescription = "Export Selected Clips",
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "Export Selected Clips to Gallery ($selectedCount)",
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 13.sp
                )
            }
        }
    }
}
""",
    )


def main() -> None:
    generate_local_properties()
    generate_gradle_files()
    generate_manifest_and_resources()
    generate_kotlin_sources()
    print("\nClipPulse Android project generated successfully!")


if __name__ == "__main__":
    main()
    sys.exit(0)
