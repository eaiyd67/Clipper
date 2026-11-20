#!/usr/bin/env python3
"""ClipPulse Android Project Generator."""
import os
import sys

PKG = "app/src/main/java/com/clippulse/studio"


def w(path: str, content: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.lstrip("\n"))
    print(f"Wrote: {path}")


def write_gradle_and_manifest() -> None:
    sdk = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if sdk:
        w("local.properties", "sdk.dir=" + sdk.replace("\\", "\\\\") + "\n")

    w("gradle.properties", r'''
org.gradle.jvmargs=-Xmx4096m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''')

    w("settings.gradle.kts", r'''
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
''')

    w("build.gradle.kts", r'''
plugins {
    id("com.android.application") version "8.7.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''')

    w("app/proguard-rules.pro", "-keep class com.yausername.** { *; }\n-dontwarn com.yausername.**\n")

    w("app/build.gradle.kts", r'''
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
        versionCode = 2
        versionName = "1.1.0"
        ndk { abiFilters += listOf("arm64-v8a", "x86_64") }
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        debug { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    packaging {
        jniLibs { useLegacyPackaging = true }
        resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" }
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
''')

    w("app/src/main/AndroidManifest.xml", r'''
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" tools:node="replace" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="29" tools:node="replace" />
    <application
        android:name=".ClipPulseApp"
        android:allowBackup="true"
        android:extractNativeLibs="true"
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@drawable/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.ClipPulse"
        android:usesCleartextTraffic="true"
        tools:replace="android:extractNativeLibs">
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
''')

    w("app/src/main/res/drawable/ic_launcher.xml", r'''
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#0B0B0F" android:pathData="M0,0h108v108h-108z" />
    <path android:fillColor="#16161D" android:pathData="M24,18h60c3.31,0 6,2.69 6,6v60c0,3.31 -2.69,6 -6,6h-60c-3.31,0 -6,-2.69 -6,-6v-60c0,-3.31 2.69,-6 6,-6z" />
    <path android:fillColor="#6366F1" android:pathData="M22,52h11l6,-18l8,36l8,-28l6,16l5,-6h20v6h-17l-9,11l-7,-18l-8,28l-8,-35l-4,14h-11z" />
    <path android:fillColor="#F59E0B" android:pathData="M78,24l2.2,4.8l5.3,0.6l-3.9,3.6l1.1,5.2l-4.7,-2.6l-4.7,2.6l1.1,-5.2l-3.9,-3.6l5.3,-0.6z" />
</vector>
''')
    w("app/src/main/res/values/strings.xml", '<?xml version="1.0" encoding="utf-8"?>\n<resources><string name="app_name">ClipPulse</string></resources>\n')
    w("app/src/main/res/values/themes.xml", '<?xml version="1.0" encoding="utf-8"?>\n<resources><style name="Theme.ClipPulse" parent="android:Theme.Material.NoActionBar"><item name="android:statusBarColor">#0B0B0F</item><item name="android:navigationBarColor">#0B0B0F</item><item name="android:windowBackground">#0B0B0F</item></style></resources>\n')


def write_core_kotlin() -> None:
    w(f"{PKG}/ClipPulseApp.kt", r'''
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
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val ch = NotificationChannel(ClipExportService.CHANNEL_ID, "ClipPulse Exports", NotificationManager.IMPORTANCE_LOW)
            getSystemService(NotificationManager::class.java)?.createNotificationChannel(ch)
        }
        appScope.launch { EngineInitializer.ensureInitialized(this@ClipPulseApp) }
    }
}
''')

    w(f"{PKG}/MainActivity.kt", r'''
package com.clippulse.studio

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.SystemBarStyle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import com.clippulse.studio.engine.UrlNormalizer
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
        handleIntent(intent)
        setContent { ClipPulseTheme { ClipPulseStudioScreen(viewModel = viewModel) } }
    }
    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIntent(intent)
    }
    private fun handleIntent(incoming: Intent?) {
        if (incoming?.action == Intent.ACTION_SEND && incoming.type == "text/plain") {
            val raw = incoming.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
            val cleanUrl = UrlNormalizer.extractAndNormalize(raw)
            if (cleanUrl.isNotBlank()) viewModel.onSharedUrlReceived(cleanUrl)
        }
    }
}
''')

    w(f"{PKG}/model/ClipModels.kt", r'''
package com.clippulse.studio.model

import androidx.compose.ui.graphics.Color
import com.clippulse.studio.ui.theme.*
import java.util.Locale

enum class AiPreset(val displayName: String, val defaultBaseUrl: String, val defaultModel: String) {
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
    val availableModels: List<String> = listOf("deepseek-chat", "deepseek-reasoner", "gemini-2.5-flash", "gemini-2.5-pro", "google/gemini-2.5-flash", "gpt-4o-mini"),
    val smartPeakOnly: Boolean = true,
    val offlineNoAiMode: Boolean = false
) {
    fun orderedKeys(): List<String> = (listOf(primaryKey.trim()) + backupKeys.map { it.trim() }).filter { it.isNotBlank() }.distinct()
    fun canUseAi(): Boolean = !offlineNoAiMode && orderedKeys().isNotEmpty() && baseUrl.isNotBlank()
}

sealed class AiConnectionState {
    data object Idle : AiConnectionState()
    data object Testing : AiConnectionState()
    data class Connected(val latencyMs: Long, val model: String) : AiConnectionState()
    data class Error(val message: String) : AiConnectionState()
}

enum class DetectionMode(val label: String) {
    SMART_ALL("All Signals"), HEATMAP("Most Replayed"), SUPER_CHAT("Super Chats"),
    CHAT_HYPE("Chat Hype"), AUDIO_PEAKS("Audio Peaks"), AI_CUSTOM("AI Custom Prompt")
}

enum class SignalSource(val label: String, val badgeColor: Color) {
    SUPER_CHAT("Super Chat", ColorGold), HEATMAP("Heatmap", ColorCrimson),
    CHAT_HYPE("Chat Hype", ColorPurple), AI_PICK("AI Pick", ColorCyan),
    TRANSCRIPT_HOOK("Transcript Hook", ElectricIndigoLight), AUDIO_PEAK("Audio Peak", ColorEmerald)
}

enum class SuperChatThreshold(val label: String, val minUsd: Double) {
    ALL("All", 0.0), PLUS_5("$5+", 5.0), PLUS_10("$10+", 10.0), PLUS_25("$25+", 25.0)
}

enum class PaddingPreset(val label: String, val beforeSec: Double, val afterSec: Double) {
    TIGHT("-2s / +3s", 2.0, 3.0), BALANCED("-3s / +5s", 3.0, 5.0),
    WIDE("-5s / +8s", 5.0, 8.0), CONTEXT("-8s / +12s", 8.0, 12.0)
}

data class HeatmapPoint(val startSec: Double, val endSec: Double, val value: Double)
data class SuperChatEvent(val donor: String, val amountDisplay: String, val usdApprox: Double, val currency: String, val message: String, val offsetSec: Double)
data class TranscriptCue(val startSec: Double, val endSec: Double, val text: String)

data class ClipCandidate(
    val id: String, val title: String, val startSec: Double, val endSec: Double,
    val hypeScore: Int, val signals: List<SignalSource>, val isMultiSignal: Boolean,
    val superChat: SuperChatEvent? = null, val transcriptQuote: String = "",
    val reason: String = "", val selected: Boolean = true
) {
    val durationSec: Double get() = (endSec - startSec).coerceAtLeast(1.0)
}

data class VideoAnalysisResult(
    val sourceUrlOrUri: String, val isLocalFile: Boolean, val localFilePath: String?,
    val videoTitle: String, val channelName: String, val durationSec: Double,
    val heatmap: List<HeatmapPoint>, val clips: List<ClipCandidate>,
    val hasLiveChat: Boolean, val hasTranscript: Boolean, val analysisSummary: String
)

enum class ExportMode(val label: String) { FAST_COPY("Fast Cut"), VERTICAL_CROP("9:16 Crop") }

sealed class ExportJobState {
    data object Idle : ExportJobState()
    data class Running(val currentIndex: Int, val total: Int, val currentTitle: String, val progressFraction: Float) : ExportJobState()
    data class Completed(val exportedCount: Int, val savedLocations: List<String>) : ExportJobState()
    data class Failed(val error: String) : ExportJobState()
}

object TimeFormatter {
    fun formatTimestamp(totalSeconds: Double): String {
        val s = totalSeconds.coerceAtLeast(0.0).toLong()
        val h = s / 3600L; val m = (s % 3600L) / 60L; val sec = s % 60L
        return if (h > 0L) String.format(Locale.US, "%02d:%02d:%02d", h, m, sec) else String.format(Locale.US, "%02d:%02d", m, sec)
    }
    fun formatFfmpegDuration(totalSeconds: Double): String {
        val c = totalSeconds.coerceAtLeast(0.0)
        return String.format(Locale.US, "%02d:%02d:%05.2f", (c / 3600.0).toInt(), ((c % 3600.0) / 60.0).toInt(), c % 60.0)
    }
    fun formatSectionTimestamp(totalSeconds: Double): String {
        val s = totalSeconds.coerceAtLeast(0.0).toLong()
        return String.format(Locale.US, "%02d:%02d:%02d", s / 3600L, (s % 3600L) / 60L, s % 60L)
    }
}
''')

    w(f"{PKG}/data/AiConfigStore.kt", r'''
package com.clippulse.studio.data

import android.content.Context
import com.clippulse.studio.model.AiConfig
import com.clippulse.studio.model.AiPreset
import org.json.JSONArray

class AiConfigStore(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences("clippulse_ai_prefs", Context.MODE_PRIVATE)
    fun load(): AiConfig {
        val preset = runCatching { AiPreset.valueOf(prefs.getString("preset", AiPreset.DEEPSEEK.name)!!) }.getOrDefault(AiPreset.DEEPSEEK)
        val savedModels = decodeList(prefs.getString("models", "[]") ?: "[]")
        return AiConfig(
            preset = preset,
            baseUrl = normalizeBaseUrl(prefs.getString("base_url", preset.defaultBaseUrl) ?: preset.defaultBaseUrl),
            primaryKey = prefs.getString("primary_key", "") ?: "",
            backupKeys = decodeList(prefs.getString("backup_keys", "[]") ?: "[]"),
            selectedModel = prefs.getString("selected_model", preset.defaultModel) ?: preset.defaultModel,
            availableModels = if (savedModels.isNotEmpty()) savedModels else AiConfig().availableModels,
            smartPeakOnly = prefs.getBoolean("smart_peak", true),
            offlineNoAiMode = prefs.getBoolean("offline_mode", false)
        )
    }
    fun save(c: AiConfig) {
        prefs.edit()
            .putString("preset", c.preset.name)
            .putString("base_url", normalizeBaseUrl(c.baseUrl))
            .putString("primary_key", c.primaryKey.trim())
            .putString("backup_keys", encodeList(c.backupKeys.filter { it.isNotBlank() }))
            .putString("selected_model", c.selectedModel.trim())
            .putString("models", encodeList(c.availableModels))
            .putBoolean("smart_peak", c.smartPeakOnly)
            .putBoolean("offline_mode", c.offlineNoAiMode)
            .apply()
    }
    private fun encodeList(items: List<String>) = JSONArray().apply { items.forEach { put(it) } }.toString()
    private fun decodeList(raw: String): List<String> = runCatching {
        val a = JSONArray(raw)
        (0 until a.length()).mapNotNull { a.optString(it).trim().takeIf { s -> s.isNotEmpty() } }
    }.getOrDefault(emptyList())

    companion object {
        fun normalizeBaseUrl(rawUrl: String): String {
            var cleaned = rawUrl.trim().trimEnd('/')
            for (suffix in listOf("/chat/completions", "/completions", "/models")) {
                if (cleaned.endsWith(suffix, ignoreCase = true)) cleaned = cleaned.dropLast(suffix.length).trimEnd('/')
            }
            return cleaned
        }
    }
}
''')

    w(f"{PKG}/network/UniversalAiClient.kt", r'''
package com.clippulse.studio.network

import android.net.Uri
import android.os.SystemClock
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.*
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

data class AiClipSuggestion(val startSec: Double, val endSec: Double, val title: String, val score: Int, val reason: String)

class UniversalAiClient {
    private val client = OkHttpClient.Builder().connectTimeout(20, TimeUnit.SECONDS).readTimeout(60, TimeUnit.SECONDS).build()
    private val jsonType = "application/json; charset=utf-8".toMediaType()

    suspend fun fetchModels(config: AiConfig): Result<List<String>> = withContext(Dispatchers.IO) {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        if (base.isBlank()) return@withContext Result.failure(IllegalArgumentException("Base URL required."))
        if (keys.isEmpty()) return@withContext Result.failure(IllegalArgumentException("Enter an API key first."))
        executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/models").get()
                .addHeader("Authorization", "Bearer $key").addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }.mapCatching { body ->
            val arr = JSONObject(body).optJSONArray("data") ?: throw IllegalStateException("Missing 'data' array.")
            val list = (0 until arr.length()).mapNotNull { arr.optJSONObject(it)?.optString("id")?.trim()?.takeIf { s -> s.isNotEmpty() } }.distinct().sorted()
            if (list.isEmpty()) throw IllegalStateException("Provider returned 0 models.")
            list
        }
    }

    suspend fun testConnection(config: AiConfig): AiConnectionState = withContext(Dispatchers.IO) {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }
        if (base.isBlank()) return@withContext AiConnectionState.Error("Base URL required.")
        if (keys.isEmpty()) return@withContext AiConnectionState.Error("No API key configured.")
        val payload = JSONObject().put("model", model).put("max_tokens", 16).put("temperature", 0.0)
            .put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", "OK"))).toString()
        val t0 = SystemClock.elapsedRealtime()
        val res = executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/chat/completions").post(payload.toRequestBody(jsonType))
                .addHeader("Authorization", "Bearer $key").addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }
        val ms = (SystemClock.elapsedRealtime() - t0).coerceAtLeast(1L)
        res.fold(onSuccess = { AiConnectionState.Connected(ms, model) }, onFailure = { AiConnectionState.Error(it.message ?: "Failed") })
    }

    suspend fun findViralAndCustomClips(
        config: AiConfig, videoTitle: String, durationSec: Double,
        cues: List<TranscriptCue>, peakCentersSec: List<Double>, customPrompt: String
    ): List<AiClipSuggestion> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || cues.isEmpty()) return@withContext emptyList()
        val selectedCues = if (config.smartPeakOnly && peakCentersSec.isNotEmpty()) {
            cues.filter { c -> peakCentersSec.any { p -> c.endSec >= p - 60.0 && c.startSec <= p + 60.0 } }
        } else cues
        val sb = StringBuilder()
        for (c in selectedCues) {
            val line = "[${String.format(Locale.US, "%.1f", c.startSec)}] ${c.text}\n"
            if (sb.length + line.length > 14000) break
            sb.append(line)
        }
        if (sb.isEmpty()) return@withContext emptyList()
        val goal = if (customPrompt.isNotBlank()) "Find moments matching: \"${customPrompt.trim()}\"." else "Find top 4 to 8 viral hooks, funny moments, or heated reactions."
        val sys = """Return STRICT JSON ONLY, no markdown or think tags: {"clips":[{"start":12.0,"end":40.0,"title":"Punchy title","score":88,"reason":"Why"}]}"""
        val usr = "Title: $videoTitle | Duration: ${TimeFormatter.formatTimestamp(durationSec)}\nTask: $goal\nTranscript:\n$sb"
        val raw = completeChat(config, sys, usr, 900) ?: return@withContext emptyList()
        val jsonStr = extractJsonObject(raw) ?: return@withContext emptyList()
        runCatching {
            val arr = JSONObject(jsonStr).optJSONArray("clips") ?: return@runCatching emptyList()
            (0 until arr.length()).mapNotNull { i ->
                val o = arr.optJSONObject(i) ?: return@mapNotNull null
                val s = o.optDouble("start", Double.NaN); val e = o.optDouble("end", Double.NaN)
                if (s.isNaN() || e.isNaN()) return@mapNotNull null
                val safeS = s.coerceIn(0.0, (durationSec - 3.0).coerceAtLeast(0.0))
                val safeE = e.coerceIn(safeS + 4.0, durationSec.coerceAtLeast(safeS + 4.0))
                AiClipSuggestion(safeS, safeE, o.optString("title").ifBlank { "AI Highlight #${i + 1}" }, o.optInt("score", 82).coerceIn(1, 100), o.optString("reason").ifBlank { "AI viral pick" })
            }
        }.getOrDefault(emptyList())
    }

    suspend fun alignSuperChatReactions(
        config: AiConfig, superChats: List<SuperChatEvent>, cues: List<TranscriptCue>, durationSec: Double
    ): Map<Double, Pair<Double, Double>> = withContext(Dispatchers.IO) {
        if (!config.canUseAi() || superChats.isEmpty() || cues.isEmpty()) return@withContext emptyMap()
        val entries = buildString {
            superChats.sortedByDescending { it.usdApprox }.take(8).forEachIndexed { idx, sc ->
                val txt = cues.filter { it.endSec >= sc.offsetSec - 15.0 && it.startSec <= sc.offsetSec + 65.0 }
                    .joinToString(" ") { "[${String.format(Locale.US, "%.1f", it.startSec)}s] ${it.text}" }.take(700)
                appendLine("Item $idx | offset=${String.format(Locale.US, "%.1f", sc.offsetSec)} | ${sc.donor} (${sc.amountDisplay}): \"${sc.message}\" | $txt")
            }
        }
        val sys = """Align Super Chat donations with streamer reaction. Return STRICT JSON ONLY: {"alignments":[{"offset":120.0,"start":116.0,"end":148.0}]}"""
        val raw = completeChat(config, sys, entries, 500) ?: return@withContext emptyMap()
        val jsonStr = extractJsonObject(raw) ?: return@withContext emptyMap()
        runCatching {
            val arr = JSONObject(jsonStr).optJSONArray("alignments") ?: return@runCatching emptyMap()
            val map = mutableMapOf<Double, Pair<Double, Double>>()
            for (i in 0 until arr.length()) {
                val o = arr.optJSONObject(i) ?: continue
                val off = o.optDouble("offset", Double.NaN); val s = o.optDouble("start", Double.NaN); val e = o.optDouble("end", Double.NaN)
                if (!off.isNaN() && !s.isNaN() && !e.isNaN() && e > s) {
                    val safeS = s.coerceIn(0.0, durationSec)
                    map[off] = safeS to e.coerceIn(safeS + 5.0, durationSec.coerceAtLeast(safeS + 5.0))
                }
            }
            map
        }.getOrDefault(emptyMap())
    }

    private fun completeChat(config: AiConfig, sys: String, usr: String, maxTokens: Int): String? {
        val base = AiConfigStore.normalizeBaseUrl(config.baseUrl)
        val keys = config.orderedKeys()
        val model = config.selectedModel.trim().ifBlank { config.preset.defaultModel }
        if (base.isBlank() || keys.isEmpty()) return null
        val payload = JSONObject().put("model", model).put("max_tokens", maxTokens).put("temperature", 0.2)
            .put("messages", JSONArray()
                .put(JSONObject().put("role", "system").put("content", sys))
                .put(JSONObject().put("role", "user").put("content", usr))).toString()
        val body = executeWithFailover(base, keys) { key ->
            Request.Builder().url("$base/chat/completions").post(payload.toRequestBody(jsonType))
                .addHeader("Authorization", "Bearer $key").addHeader("Content-Type", "application/json")
                .addHeader("HTTP-Referer", "https://clippulse.app").addHeader("X-Title", "ClipPulse").build()
        }.getOrNull() ?: return null
        return runCatching { JSONObject(body).getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content").trim() }.getOrNull()
    }

    private fun extractJsonObject(raw: String): String? {
        val cleaned = raw.replace(Regex("""<think>[\s\S]*?</think>""", RegexOption.IGNORE_CASE), "")
            .replace("```json", "", ignoreCase = true).replace("```", "").trim()
        return Regex("""\{[\s\S]*\}""").find(cleaned)?.value
    }

    private fun executeWithFailover(baseUrl: String, keys: List<String>, reqFactory: (String) -> Request): Result<String> {
        var lastErr = "Request failed"
        val host = runCatching { Uri.parse(baseUrl).host }.getOrNull().orEmpty().ifBlank { baseUrl }
        for ((idx, key) in keys.withIndex()) {
            try {
                client.newCall(reqFactory(key)).execute().use { resp ->
                    val bodyStr = resp.body?.string().orEmpty()
                    if (resp.isSuccessful) return Result.success(bodyStr)
                    val msg = runCatching { JSONObject(bodyStr).optJSONObject("error")?.optString("message") }.getOrNull()?.takeIf { it.isNotBlank() } ?: resp.message
                    lastErr = if (resp.code == 402) {
                        "Key #${idx + 1} ($host): HTTP 402 ($msg) — check provider balance or switch preset (e.g. Gemini)"
                    } else {
                        "Key #${idx + 1} ($host): HTTP ${resp.code} ($msg)"
                    }
                    val rotatable = resp.code == 401 || resp.code == 402 || resp.code == 403 || resp.code == 429 || resp.code in 500..599
                    if (!rotatable || idx == keys.lastIndex) {
                        return Result.failure(IllegalStateException(lastErr))
                    }
                }
            } catch (e: Throwable) {
                lastErr = e.message ?: "Network error"
                if (idx == keys.lastIndex) return Result.failure(IllegalStateException(lastErr))
            }
        }
        return Result.failure(IllegalStateException(lastErr))
    }
}
''')
def write_engines_and_service() -> None:
    w(f"{PKG}/engine/UrlNormalizer.kt", r'''
package com.clippulse.studio.engine

import android.net.Uri

object UrlNormalizer {
    /**
     * Extracts the first URL from shared text and normalizes YouTube app /live/, /shorts/,
     * and youtu.be/?si= links into canonical https://www.youtube.com/watch?v=VIDEO_ID URLs.
     */
    fun extractAndNormalize(rawInput: String): String {
        val extracted = Regex("""https?://\S+""").find(rawInput.trim())?.value
            ?.trimEnd('.', ',', ')', ']', '"', '\'')
            ?: rawInput.trim()
        if (extracted.isBlank()) return ""

        val uri = runCatching { Uri.parse(extracted) }.getOrNull() ?: return extracted
        val host = uri.host?.lowercase().orEmpty()
        val segments = uri.pathSegments.orEmpty()

        val youtubeVideoId: String? = when {
            host == "youtu.be" || host.endsWith(".youtu.be") -> segments.firstOrNull()
            host.contains("youtube.com") -> when {
                segments.firstOrNull() == "watch" -> uri.getQueryParameter("v")
                segments.firstOrNull() == "live" && segments.size >= 2 -> segments[1]
                segments.firstOrNull() == "shorts" && segments.size >= 2 -> segments[1]
                segments.firstOrNull() == "embed" && segments.size >= 2 -> segments[1]
                else -> null
            }
            else -> null
        }

        return if (!youtubeVideoId.isNullOrBlank()) {
            val cleanId = youtubeVideoId.takeWhile { it.isLetterOrDigit() || it == '-' || it == '_' }
            if (cleanId.isNotBlank()) "https://www.youtube.com/watch?v=$cleanId" else extracted
        } else {
            extracted
        }
    }
}
''')

    w(f"{PKG}/engine/EngineInitializer.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import com.yausername.ffmpeg.FFmpeg
import com.yausername.youtubedl_android.YoutubeDL

object EngineInitializer {
    @Volatile private var initialized = false
    private val lock = Any()

    fun ensureInitialized(context: Context): Result<Unit> {
        if (initialized) return Result.success(Unit)
        synchronized(lock) {
            if (initialized) return Result.success(Unit)
            return runCatching {
                val app = context.applicationContext
                YoutubeDL.getInstance().init(app)
                FFmpeg.getInstance().init(app)
                initialized = true
            }
        }
    }

    fun updateYtDlpEngine(context: Context): Result<String> = runCatching {
        ensureInitialized(context).getOrThrow()
        YoutubeDL.getInstance().updateYoutubeDL(context.applicationContext)?.toString() ?: "UPDATED"
    }
}
''')

    w(f"{PKG}/engine/FfmpegRunner.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets

object FfmpegRunner {
    fun run(context: Context, args: List<String>, onLine: ((String) -> Unit)? = null): Result<Unit> = runCatching {
        EngineInitializer.ensureInitialized(context).getOrThrow()
        val nativeDir = context.applicationInfo.nativeLibraryDir
        val bin = File(nativeDir, "libffmpeg.so").takeIf { it.exists() }
            ?: File(context.noBackupFilesDir, "youtubedl-android/packages/ffmpeg/usr/bin/ffmpeg").takeIf { it.exists() }
            ?: throw IllegalStateException("FFmpeg binary not found in $nativeDir")
        val cmd = ArrayList<String>(args.size + 1).apply { add(bin.absolutePath); addAll(args) }
        val pb = ProcessBuilder(cmd).apply {
            redirectErrorStream(true)
            val ld = environment()["LD_LIBRARY_PATH"].orEmpty()
            environment()["LD_LIBRARY_PATH"] = if (ld.isBlank()) nativeDir else "$nativeDir:$ld"
        }
        val proc = pb.start()
        val tail = ArrayDeque<String>(20)
        BufferedReader(InputStreamReader(proc.inputStream, StandardCharsets.UTF_8), 32768).use { r ->
            var line = r.readLine()
            while (line != null) {
                onLine?.invoke(line)
                if (tail.size >= 20) tail.removeFirst()
                tail.addLast(line)
                line = r.readLine()
            }
        }
        val code = proc.waitFor()
        if (code != 0) throw IllegalStateException("FFmpeg exit $code: ${tail.joinToString("\n").takeLast(350)}")
    }
}
''')

    w(f"{PKG}/engine/SubtitleAndChatParser.kt", r'''
package com.clippulse.studio.engine

import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.SignalSource
import com.clippulse.studio.model.SuperChatEvent
import com.clippulse.studio.model.TranscriptCue
import org.json.JSONObject
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.InputStreamReader
import java.nio.charset.StandardCharsets
import java.util.Locale
import java.util.UUID
import kotlin.math.sqrt

data class ChatVelocitySpike(val startSec: Double, val endSec: Double, val messageCount: Int, val multiplierOverAvg: Double)
data class LiveChatParseOutput(val superChats: List<SuperChatEvent>, val velocitySpikes: List<ChatVelocitySpike>, val totalMessagesParsed: Int)

object SubtitleAndChatParser {
    fun parseLiveChatStreaming(chatFile: File, durationSec: Double): LiveChatParseOutput {
        if (!chatFile.exists() || chatFile.length() == 0L) return LiveChatParseOutput(emptyList(), emptyList(), 0)
        val superChats = mutableListOf<SuperChatEvent>()
        val buckets = HashMap<Int, Int>()
        var total = 0
        BufferedReader(InputStreamReader(FileInputStream(chatFile), StandardCharsets.UTF_8), 65536).use { reader ->
            var line = reader.readLine()
            while (line != null) {
                val t = line.trim()
                if (t.startsWith("{")) total += parseChatLine(t, durationSec, superChats, buckets)
                line = reader.readLine()
            }
        }
        return LiveChatParseOutput(superChats.sortedBy { it.offsetSec }, detectSpikes(buckets, durationSec), total)
    }

    private fun parseChatLine(jsonLine: String, durationSec: Double, scOut: MutableList<SuperChatEvent>, buckets: MutableMap<Int, Int>): Int {
        return try {
            val replay = JSONObject(jsonLine).optJSONObject("replayChatItemAction") ?: return 0
            val offsetMs = replay.optString("videoOffsetTimeMsec", "").toLongOrNull() ?: return 0
            if (offsetMs < 0L) return 0
            val offsetSec = offsetMs / 1000.0
            if (durationSec > 0.0 && offsetSec > durationSec + 30.0) return 0
            val actions = replay.optJSONArray("actions") ?: return 0
            val bucket = (offsetSec / 10.0).toInt().coerceAtLeast(0)
            var count = 0
            for (i in 0 until actions.length()) {
                val item = actions.optJSONObject(i)?.optJSONObject("addChatItemAction")?.optJSONObject("item") ?: continue
                val paid = item.optJSONObject("liveChatPaidMessageRenderer")
                val sticker = item.optJSONObject("liveChatPaidStickerRenderer")
                val text = item.optJSONObject("liveChatTextMessageRenderer")
                val member = item.optJSONObject("liveChatMembershipItemRenderer")
                if (paid != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                    extractSuperChat(paid, offsetSec, false)?.let { scOut.add(it) }
                } else if (sticker != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                    extractSuperChat(sticker, offsetSec, true)?.let { scOut.add(it) }
                } else if (text != null || member != null) {
                    count++; buckets[bucket] = (buckets[bucket] ?: 0) + 1
                }
            }
            count
        } catch (_: Throwable) { 0 }
    }

    private fun extractSuperChat(r: JSONObject, offsetSec: Double, isSticker: Boolean): SuperChatEvent? {
        val donor = r.optJSONObject("authorName")?.optString("simpleText")?.trim()?.takeIf { it.isNotEmpty() } ?: "Supporter"
        val amt = r.optJSONObject("purchaseAmountText")?.optString("simpleText")?.trim()?.takeIf { it.isNotEmpty() } ?: return null
        val runs = r.optJSONObject("message")?.optJSONArray("runs")
        val msg = buildString { if (runs != null) for (i in 0 until runs.length()) append(runs.optJSONObject(i)?.optString("text").orEmpty()) }
            .trim().ifBlank { if (isSticker) "[Super Sticker]" else "" }
        val rawVal = Regex("""(\d+(?:\.\d+)?)""").find(amt.replace(",", ""))?.groupValues?.getOrNull(1)?.toDoubleOrNull() ?: 1.0
        val (cur, usd) = when {
            amt.contains("¥") || amt.contains("JPY", true) -> "JPY" to rawVal / 150.0
            amt.contains("₩") || amt.contains("KRW", true) -> "KRW" to rawVal / 1380.0
            amt.contains("₹") || amt.contains("INR", true) -> "INR" to rawVal / 84.0
            amt.contains("€") || amt.contains("EUR", true) -> "EUR" to rawVal * 1.08
            amt.contains("£") || amt.contains("GBP", true) -> "GBP" to rawVal * 1.27
            else -> "USD" to rawVal
        }
        return SuperChatEvent(donor, amt, usd, cur, msg, offsetSec)
    }

    private fun detectSpikes(buckets: Map<Int, Int>, durationSec: Double): List<ChatVelocitySpike> {
        if (buckets.size < 4) return emptyList()
        val vals = buckets.values.map { it.toDouble() }
        val mean = vals.average()
        val std = sqrt(vals.sumOf { (it - mean) * (it - mean) } / vals.size.toDouble())
        val threshold = maxOf(6.0, mean + 2.1 * std)
        val spiked = buckets.entries.filter { it.value.toDouble() >= threshold }.sortedBy { it.key }
        if (spiked.isEmpty()) return emptyList()
        val merged = mutableListOf<ChatVelocitySpike>()
        var sB = spiked.first().key; var eB = sB; var peak = spiked.first().value
        for (i in 1 until spiked.size) {
            val (b, c) = spiked[i]
            if (b <= eB + 2) { eB = b; if (c > peak) peak = c }
            else { merged.add(makeSpike(sB, eB, peak, mean, durationSec)); sB = b; eB = b; peak = c }
        }
        merged.add(makeSpike(sB, eB, peak, mean, durationSec))
        return merged.sortedByDescending { it.messageCount }.take(12)
    }

    private fun makeSpike(sB: Int, eB: Int, peak: Int, mean: Double, dur: Double): ChatVelocitySpike {
        val s = (sB * 10.0).coerceAtLeast(0.0)
        val rawE = (eB + 1) * 10.0
        val e = if (dur > 0.0) rawE.coerceAtMost(dur) else rawE
        return ChatVelocitySpike(s, e.coerceAtLeast(s + 10.0), peak, if (mean > 0.1) peak.toDouble() / mean else 3.0)
    }

    fun parseVttSubtitles(vttFile: File): List<TranscriptCue> {
        if (!vttFile.exists()) return emptyList()
        val raw = mutableListOf<TranscriptCue>()
        val timeRe = Regex("""(?:(\d+):)?(\d{2}):(\d{2}\.\d+)\s*-->\s*(?:(\d+):)?(\d{2}):(\d{2}\.\d+)""")
        val tagRe = Regex("""<[^>]+>""")
        var curS: Double? = null; var curE: Double? = null; val buf = StringBuilder()
        vttFile.forEachLine(StandardCharsets.UTF_8) { rawLine ->
            val line = rawLine.trim()
            val m = timeRe.find(line)
            if (m != null) {
                if (curS != null && curE != null && buf.isNotEmpty()) raw.add(TranscriptCue(curS!!, curE!!, buf.toString().trim()))
                buf.clear()
                curS = (m.groupValues[1].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[2].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[3].toDoubleOrNull() ?: 0.0)
                curE = (m.groupValues[4].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[5].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[6].toDoubleOrNull() ?: 0.0)
            } else if (line.isNotEmpty() && !line.startsWith("WEBVTT") && !line.startsWith("Kind:") && !line.startsWith("Language:") && line.toIntOrNull() == null) {
                val clean = line.replace(tagRe, "").replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&#39;", "'").replace("&quot;", "\"").trim()
                if (clean.isNotEmpty()) { if (buf.isNotEmpty()) buf.append(' '); buf.append(clean) }
            }
        }
        if (curS != null && curE != null && buf.isNotEmpty()) raw.add(TranscriptCue(curS!!, curE!!, buf.toString().trim()))
        val dedup = mutableListOf<TranscriptCue>()
        for (c in raw) {
            val prev = dedup.lastOrNull()
            if (prev != null && (prev.text == c.text || c.text.startsWith(prev.text))) dedup[dedup.lastIndex] = c.copy(startSec = prev.startSec)
            else dedup.add(c)
        }
        return dedup
    }

    /**
     * Offline Transcript Excitement & Hook Scanner:
     * Scores 25-second windows by speech-rate surges, crowd/laughter markers, and high-energy reaction phrases.
     */
    fun detectTranscriptExcitementPeaks(cues: List<TranscriptCue>, durationSec: Double): List<ClipCandidate> {
        if (cues.isEmpty()) return emptyList()
        val windowSec = 25.0
        val bucketCount = ((durationSec / windowSec).toInt() + 1).coerceIn(1, 720)
        val windowText = Array(bucketCount) { StringBuilder() }
        val windowWords = IntArray(bucketCount)

        for (cue in cues) {
            val idx = (cue.startSec / windowSec).toInt().coerceIn(0, bucketCount - 1)
            val words = cue.text.split(Regex("""\s+""")).count { it.isNotBlank() }
            windowWords[idx] += words
            if (windowText[idx].length < 400) {
                if (windowText[idx].isNotEmpty()) windowText[idx].append(' ')
                windowText[idx].append(cue.text)
            }
        }

        val activeCounts = windowWords.filter { it > 0 }.map { it.toDouble() }
        if (activeCounts.isEmpty()) return emptyList()
        val avgWords = activeCounts.average().coerceAtLeast(8.0)

        val hypePhrases = listOf(
            "no way", "oh my god", "omg", "what the", "are you serious", "let's go", "lets go",
            "bro", "insane", "crazy", "unbelievable", "wait a minute", "hold on", "listen",
            "laugh", "applause", "cheer", "goal", "retired", "impossible", "secret", "truth"
        )

        data class ScoredWindow(val idx: Int, val energy: Double, val title: String, val reason: String)
        val scored = mutableListOf<ScoredWindow>()

        for (i in 0 until bucketCount) {
            val wCount = windowWords[i]
            if (wCount < 6) continue
            val text = windowText[i].toString()
            val lower = text.lowercase(Locale.US)
            val paceRatio = wCount.toDouble() / avgWords
            val exclCount = text.count { it == '!' || it == '?' }
            val bracketTags = Regex("""\[(?:laughter|applause|cheering|music)]""", RegexOption.IGNORE_CASE).findAll(text).count()
            val phraseHits = hypePhrases.count { lower.contains(it) }

            val energy = (paceRatio * 1.4) + (exclCount * 0.35) + (bracketTags * 1.2) + (phraseHits * 0.55)
            val snippet = text.replace(Regex("""\[[^\]]+]"""), "").trim().take(52)
            val title = if (snippet.length >= 12) "\"$snippet...\"" else "Spoken Excitement Spike #${i + 1}"
            val reason = String.format(Locale.US, "High vocal energy (%.1fx speech pace, %d hype cues)", paceRatio, phraseHits + bracketTags)
            scored.add(ScoredWindow(i, energy, title, reason))
        }

        if (scored.isEmpty()) return emptyList()
        val maxEnergy = scored.maxOf { it.energy }.coerceAtLeast(1.0)

        return scored.sortedByDescending { it.energy }.take(10).map { sw ->
            val start = (sw.idx * windowSec).coerceAtLeast(0.0)
            val end = ((sw.idx + 1) * windowSec + 5.0).coerceAtMost(durationSec)
            val norm = (sw.energy / maxEnergy).coerceIn(0.0, 1.0)
            val score = (68 + (norm * 26.0).toInt()).coerceIn(68, 94)
            ClipCandidate(
                id = UUID.randomUUID().toString(),
                title = sw.title,
                startSec = start,
                endSec = end.coerceAtLeast((start + 5.0).coerceAtMost(durationSec)),
                hypeScore = score,
                signals = listOf(SignalSource.TRANSCRIPT_HOOK),
                isMultiSignal = false,
                reason = sw.reason
            )
        }
    }

    fun extractQuoteAround(cues: List<TranscriptCue>, startSec: Double, endSec: Double): String =
        cues.filter { it.endSec >= startSec && it.startSec <= endSec }.joinToString(" ") { it.text }.trim().take(220)
}
''')

    w(f"{PKG}/engine/VideoAnalysisEngine.kt", r'''
package com.clippulse.studio.engine

import android.content.Context
import android.media.MediaMetadataRetriever
import android.net.Uri
import android.provider.OpenableColumns
import com.clippulse.studio.model.*
import com.clippulse.studio.network.UniversalAiClient
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

class VideoAnalysisEngine(private val aiClient: UniversalAiClient = UniversalAiClient()) {

    suspend fun analyzeRemoteUrl(
        context: Context, rawUrl: String, mode: DetectionMode, superChatThreshold: SuperChatThreshold,
        paddingPreset: PaddingPreset, customAiPrompt: String, aiConfig: AiConfig, onProgress: (Float, String) -> Unit
    ): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            val cleanUrl = UrlNormalizer.extractAndNormalize(rawUrl)
            if (cleanUrl.isBlank()) return@withContext Result.failure(IllegalArgumentException("Enter a valid YouTube or Facebook link."))

            onProgress(0.10f, "Initializing yt-dlp zero-download engine...")
            EngineInitializer.ensureInitialized(context).getOrThrow()
            val workDir = File(context.cacheDir, "analysis_${System.currentTimeMillis()}").apply { mkdirs() }
            try {
                onProgress(0.24f, "Fetching metadata, heatmap & captions (zero download)...")
                fetchMetadataAndCaptions(cleanUrl, workDir)

                val infoFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".info.json") }
                    ?: return@withContext Result.failure(IllegalStateException("Could not read video metadata. Tap 'Update yt-dlp' in AI Settings or check link."))

                onProgress(0.42f, "Parsing replay heatmap & chapter cues...")
                val info = JSONObject(infoFile.readText(Charsets.UTF_8))
                val title = info.optString("title").ifBlank { "Untitled Video" }
                val channel = info.optString("uploader").ifBlank { info.optString("channel").ifBlank { "Creator" } }
                val duration = info.optDouble("duration", 0.0).coerceAtLeast(1.0)
                val wasLive = info.optBoolean("was_live", false) || info.optString("live_status") in listOf("was_live", "post_live")

                val heatmap = parseHeatmap(info)
                val raw = mutableListOf<ClipCandidate>()
                if (heatmap.isNotEmpty()) raw.addAll(detectHeatmapPeaks(heatmap, duration))
                else raw.addAll(detectChaptersAndDesc(info, duration))

                // Non-blocking second pass for live chat replay on streams/VODs
                var allSc = emptyList<SuperChatEvent>()
                var chatFile: File? = null
                if (wasLive || mode == DetectionMode.SUPER_CHAT || mode == DetectionMode.CHAT_HYPE || mode == DetectionMode.SMART_ALL) {
                    onProgress(0.56f, "Checking live chat replay & Super Chats...")
                    runCatching {
                        val chatReq = YoutubeDLRequest(cleanUrl).apply {
                            addOption("--skip-download"); addOption("--write-subs"); addOption("--sub-langs", "live_chat")
                            addOption("--no-playlist"); addOption("--no-warnings"); addOption("--ignore-errors")
                            addOption("-o", File(workDir, "chat.%(ext)s").absolutePath)
                        }
                        YoutubeDL.getInstance().execute(chatReq)
                    }
                    chatFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".live_chat.json") }
                    if (chatFile != null) {
                        val out = SubtitleAndChatParser.parseLiveChatStreaming(chatFile, duration)
                        allSc = out.superChats
                        for (sp in out.velocitySpikes) {
                            raw.add(ClipCandidate(UUID.randomUUID().toString(), "Chat Hype Surge (${sp.messageCount} msgs/10s)",
                                (sp.startSec - 4.0).coerceAtLeast(0.0), (sp.endSec + 10.0).coerceAtMost(duration),
                                (70 + (sp.multiplierOverAvg * 6.0).toInt()).coerceIn(65, 96), listOf(SignalSource.CHAT_HYPE), false,
                                reason = String.format(Locale.US, "Chat spiked %.1fx above average", sp.multiplierOverAvg)))
                        }
                    }
                }

                onProgress(0.70f, "Indexing transcript cues...")
                val vttFile = workDir.listFiles()?.firstOrNull { it.name.endsWith(".vtt") }
                val cues = if (vttFile != null) SubtitleAndChatParser.parseVttSubtitles(vttFile) else emptyList()

                val filteredSc = allSc.filter { it.usdApprox >= superChatThreshold.minUsd }
                val aligned = if (aiConfig.canUseAi() && filteredSc.isNotEmpty() && cues.isNotEmpty()) {
                    onProgress(0.78f, "AI-aligning Super Chat donor reactions...")
                    aiClient.alignSuperChatReactions(aiConfig, filteredSc, cues, duration)
                } else emptyMap()

                for (sc in filteredSc) {
                    val rng = aligned[sc.offsetSec]
                    val s = rng?.first ?: (sc.offsetSec - 4.0).coerceAtLeast(0.0)
                    val e = rng?.second ?: (sc.offsetSec + 22.0).coerceAtMost(duration)
                    val score = when { sc.usdApprox >= 50.0 -> 95; sc.usdApprox >= 25.0 -> 90; sc.usdApprox >= 10.0 -> 84; sc.usdApprox >= 5.0 -> 78; else -> 72 }
                    raw.add(ClipCandidate(UUID.randomUUID().toString(), "${sc.donor} • ${sc.amountDisplay}", s, e, score,
                        listOf(SignalSource.SUPER_CHAT), false, superChat = sc, reason = "Super Chat highlight (${sc.amountDisplay})"))
                }

                if (aiConfig.canUseAi() && cues.isNotEmpty() && (mode == DetectionMode.SMART_ALL || mode == DetectionMode.AI_CUSTOM)) {
                    onProgress(0.86f, "Running AI viral hook & prompt scan...")
                    val picks = aiClient.findViralAndCustomClips(aiConfig, title, duration, cues, raw.map { (it.startSec + it.endSec) / 2.0 },
                        if (mode == DetectionMode.AI_CUSTOM) customAiPrompt else "")
                    for (p in picks) {
                        raw.add(ClipCandidate(UUID.randomUUID().toString(), p.title, p.startSec, p.endSec, p.score, listOf(SignalSource.AI_PICK), false, reason = p.reason))
                    }
                }

                // Offline Transcript Hook Scanner: guarantees clips when Heatmap/Chat/AI return fewer than 3 clips
                if (cues.isNotEmpty() && raw.size < 3) {
                    onProgress(0.91f, "Scanning transcript for excitement & speech spikes...")
                    raw.addAll(SubtitleAndChatParser.detectTranscriptExcitementPeaks(cues, duration))
                }

                onProgress(0.96f, "Merging multi-signal consensus clips...")
                val modeFiltered = when (mode) {
                    DetectionMode.SMART_ALL -> raw
                    DetectionMode.HEATMAP -> raw.filter { SignalSource.HEATMAP in it.signals }
                    DetectionMode.SUPER_CHAT -> raw.filter { SignalSource.SUPER_CHAT in it.signals }
                    DetectionMode.CHAT_HYPE -> raw.filter { SignalSource.CHAT_HYPE in it.signals }
                    DetectionMode.AUDIO_PEAKS -> raw.filter { SignalSource.AUDIO_PEAK in it.signals }
                    DetectionMode.AI_CUSTOM -> raw.filter { SignalSource.AI_PICK in it.signals }
                }
                // If user picked a single filter (e.g. Super Chats) that had 0 matches, fall back to all detected clips
                val effectiveList = if (modeFiltered.isNotEmpty()) modeFiltered else raw
                val consensus = runConsensus(effectiveList, cues, paddingPreset, duration)

                val summary = buildString {
                    append("${consensus.size} clips found")
                    if (heatmap.isNotEmpty()) append(" • Heatmap")
                    if (allSc.isNotEmpty()) append(" • ${allSc.size} Super Chats")
                    if (cues.isNotEmpty()) append(" • Transcript")
                    if (modeFiltered.isEmpty() && raw.isNotEmpty()) append(" (auto-fallback from ${mode.label})")
                }
                onProgress(1.0f, "Done!")
                Result.success(VideoAnalysisResult(cleanUrl, false, null, title, channel, duration, heatmap, consensus, chatFile != null, cues.isNotEmpty(), summary))
            } finally { workDir.deleteRecursively() }
        } catch (t: Throwable) { Result.failure(t) }
    }

    private fun fetchMetadataAndCaptions(cleanUrl: String, workDir: File) {
        val outPath = File(workDir, "meta.%(ext)s").absolutePath
        val primaryAttempt = runCatching {
            val req = YoutubeDLRequest(cleanUrl).apply {
                addOption("--skip-download"); addOption("--write-info-json")
                addOption("--write-auto-sub"); addOption("--write-subs"); addOption("--sub-langs", "en.*,en")
                addOption("--extractor-args", "youtube:player_client=android,web")
                addOption("--no-playlist"); addOption("--no-warnings"); addOption("--ignore-errors")
                addOption("-o", outPath)
            }
            YoutubeDL.getInstance().execute(req)
        }
        val hasInfo = workDir.listFiles()?.any { it.name.endsWith(".info.json") } == true
        if (!hasInfo) {
            // Fallback player clients for recently ended YouTube livestreams & mobile share links
            val fallbackReq = YoutubeDLRequest(cleanUrl).apply {
                addOption("--skip-download"); addOption("--write-info-json")
                addOption("--write-auto-sub"); addOption("--write-subs"); addOption("--sub-langs", "en.*,en")
                addOption("--extractor-args", "youtube:player_client=tv,mweb,ios")
                addOption("--no-playlist"); addOption("--no-warnings"); addOption("--ignore-errors")
                addOption("-o", outPath)
            }
            runCatching { YoutubeDL.getInstance().execute(fallbackReq) }
            if (workDir.listFiles()?.none { it.name.endsWith(".info.json") } == true) {
                primaryAttempt.getOrThrow()
            }
        }
    }

    suspend fun analyzeLocalVideo(context: Context, uri: Uri, paddingPreset: PaddingPreset, onProgress: (Float, String) -> Unit): Result<VideoAnalysisResult> = withContext(Dispatchers.IO) {
        try {
            onProgress(0.15f, "Staging local video...")
            val localDir = File(context.cacheDir, "local_videos").apply { mkdirs(); listFiles()?.forEach { it.delete() } }
            val name = context.contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { c ->
                if (c.moveToFirst()) c.getString(0) else null
            } ?: "local_input.mp4"
            val staged = File(localDir, name)
            context.contentResolver.openInputStream(uri)?.use { inp -> FileOutputStream(staged).use { out -> inp.copyTo(out, 65536) } }
                ?: return@withContext Result.failure(IllegalStateException("Cannot read selected local video."))
            val retriever = MediaMetadataRetriever()
            val duration = try {
                retriever.setDataSource(staged.absolutePath)
                (retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)?.toLongOrNull() ?: 0L) / 1000.0
            } finally { runCatching { retriever.release() } }.coerceAtLeast(1.0)

            onProgress(0.50f, "Scanning audio RMS energy spikes with FFmpeg...")
            val ptsRe = Regex("""pts_time:(\d+(?:\.\d+)?)"""); val rmsRe = Regex("""RMS level dB:\s*(-?\d+(?:\.\d+)?)""")
            val samples = mutableListOf<Pair<Double, Double>>(); var latestPts = 0.0
            FfmpegRunner.run(context, listOf("-hide_banner", "-i", staged.absolutePath, "-af", "astats=metadata=1:reset=1", "-f", "null", "-")) { line ->
                ptsRe.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { latestPts = it }
                rmsRe.find(line)?.groupValues?.getOrNull(1)?.toDoubleOrNull()?.let { db -> if (db.isFinite() && db > -90.0) samples.add(latestPts to db) }
            }
            onProgress(0.85f, "Building acoustic energy peaks...")
            val (heatmap, peaks) = buildAudioPeaks(samples, duration)
            val consensus = runConsensus(peaks, emptyList(), paddingPreset, duration)
            onProgress(1.0f, "Done!")
            Result.success(VideoAnalysisResult(uri.toString(), true, staged.absolutePath, staged.nameWithoutExtension, "Local Device Video", duration, heatmap, consensus, false, false, "${consensus.size} audio peaks"))
        } catch (t: Throwable) { Result.failure(t) }
    }

    private fun parseHeatmap(info: JSONObject): List<HeatmapPoint> {
        val arr = info.optJSONArray("heatmap") ?: return emptyList()
        return (0 until arr.length()).mapNotNull { i ->
            val o = arr.optJSONObject(i) ?: return@mapNotNull null
            val s = o.optDouble("start_time", Double.NaN); val e = o.optDouble("end_time", Double.NaN); val v = o.optDouble("value", Double.NaN)
            if (!s.isNaN() && !e.isNaN() && !v.isNaN()) HeatmapPoint(s, e, v.coerceIn(0.0, 1.0)) else null
        }
    }

    private fun detectHeatmapPeaks(hm: List<HeatmapPoint>, dur: Double): List<ClipCandidate> {
        if (hm.size < 3) return emptyList()
        val out = mutableListOf<ClipCandidate>()
        for (i in 1 until hm.lastIndex) {
            val c = hm[i].value
            if (c >= 0.62 && c >= hm[i - 1].value && c >= hm[i + 1].value) {
                val center = (hm[i].startSec + hm[i].endSec) / 2.0
                out.add(ClipCandidate(UUID.randomUUID().toString(), "Most Replayed Spike (${(c * 100.0).toInt()}%)",
                    (center - 12.0).coerceAtLeast(0.0), (center + 18.0).coerceAtMost(dur),
                    (60 + (c * 38.0).toInt()).coerceIn(60, 98), listOf(SignalSource.HEATMAP), false, reason = "Replay intensity ${(c * 100.0).toInt()}%"))
            }
        }
        return out.sortedByDescending { it.hypeScore }.take(12)
    }

    private fun detectChaptersAndDesc(info: JSONObject, dur: Double): List<ClipCandidate> {
        val chs = info.optJSONArray("chapters")
        if (chs != null && chs.length() > 0) {
            return (0 until chs.length().coerceAtMost(12)).mapNotNull { i ->
                val o = chs.optJSONObject(i) ?: return@mapNotNull null
                val s = o.optDouble("start_time", Double.NaN); val e = o.optDouble("end_time", Double.NaN)
                if (!s.isNaN() && !e.isNaN() && e > s) ClipCandidate(UUID.randomUUID().toString(), o.optString("title").ifBlank { "Chapter #${i + 1}" },
                    s.coerceAtLeast(0.0), minOf(e, s + 45.0).coerceAtMost(dur), 74, listOf(SignalSource.HEATMAP), false, reason = "Chapter marker") else null
            }
        }
        return Regex("""(?m)^(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\s+(.+)$""").findAll(info.optString("description")).take(10).map { m ->
            val s = ((m.groupValues[1].toDoubleOrNull() ?: 0.0) * 3600.0 + (m.groupValues[2].toDoubleOrNull() ?: 0.0) * 60.0 + (m.groupValues[3].toDoubleOrNull() ?: 0.0)).coerceIn(0.0, (dur - 5.0).coerceAtLeast(0.0))
            ClipCandidate(UUID.randomUUID().toString(), m.groupValues[4].trim().take(60), s, (s + 30.0).coerceAtMost(dur), 72, listOf(SignalSource.HEATMAP), false, reason = "Description timestamp")
        }.toList()
    }

    private fun buildAudioPeaks(samples: List<Pair<Double, Double>>, dur: Double): Pair<List<HeatmapPoint>, List<ClipCandidate>> {
        if (samples.isEmpty()) return emptyList<HeatmapPoint>() to listOf(ClipCandidate(UUID.randomUUID().toString(), "Opening Highlight", 0.0, minOf(25.0, dur), 70, listOf(SignalSource.AUDIO_PEAK), false, reason = "Default segment"))
        val count = 40; val bSize = (dur / count.toDouble()).coerceAtLeast(1.0); val maxDb = DoubleArray(count) { -60.0 }
        for ((t, db) in samples) { val idx = (t / bSize).toInt().coerceIn(0, count - 1); if (db > maxDb[idx]) maxDb[idx] = db }
        val minV = maxDb.minOrNull() ?: -60.0; val maxV = maxDb.maxOrNull() ?: -10.0; val span = (maxV - minV).coerceAtLeast(1.0)
        val hm = (0 until count).map { i -> HeatmapPoint(i * bSize, minOf((i + 1) * bSize, dur), ((maxDb[i] - minV) / span).coerceIn(0.05, 1.0)) }
        val mean = maxDb.average(); val thresh = mean + 1.15 * sqrt(maxDb.sumOf { (it - mean) * (it - mean) } / count.toDouble())
        val peaks = (0 until count).filter { maxDb[it] >= thresh }.map { i ->
            val c = (i + 0.5) * bSize; val norm = ((maxDb[i] - minV) / span).coerceIn(0.0, 1.0)
            ClipCandidate(UUID.randomUUID().toString(), String.format(Locale.US, "Audio Peak (%.1f dB)", maxDb[i]),
                (c - 8.0).coerceAtLeast(0.0), (c + 14.0).coerceAtMost(dur), (68 + (norm * 29.0).toInt()).coerceIn(68, 97),
                listOf(SignalSource.AUDIO_PEAK), false, reason = String.format(Locale.US, "+%.1f dB above baseline", maxDb[i] - mean))
        }.sortedByDescending { it.hypeScore }.take(12)
        return hm to peaks
    }

    private fun runConsensus(cands: List<ClipCandidate>, cues: List<TranscriptCue>, pad: PaddingPreset, dur: Double): List<ClipCandidate> {
        if (cands.isEmpty()) return emptyList()
        val sorted = cands.sortedBy { it.startSec }; val merged = mutableListOf<ClipCandidate>(); var cur = sorted.first()
        for (i in 1 until sorted.size) {
            val nxt = sorted[i]
            if (nxt.startSec - cur.endSec <= 18.0) {
                val sigs = (cur.signals + nxt.signals).distinct(); val multi = sigs.size >= 2
                val score = if (multi) (maxOf(cur.hypeScore, nxt.hypeScore) + 11 * (sigs.size - 1)).coerceIn(1, 100) else maxOf(cur.hypeScore, nxt.hypeScore)
                val sc = cur.superChat ?: nxt.superChat
                val title = when { sc != null -> "${sc.donor} • ${sc.amountDisplay}"; nxt.hypeScore > cur.hypeScore -> nxt.title; else -> cur.title }
                cur = cur.copy(title = title, startSec = minOf(cur.startSec, nxt.startSec), endSec = maxOf(cur.endSec, nxt.endSec),
                    hypeScore = score, signals = sigs, isMultiSignal = multi, superChat = sc, reason = listOf(cur.reason, nxt.reason).filter { it.isNotBlank() }.distinct().joinToString(" + "))
            } else { merged.add(finalizeClip(cur, cues, pad, dur)); cur = nxt }
        }
        merged.add(finalizeClip(cur, cues, pad, dur))
        return merged.sortedWith(compareByDescending<ClipCandidate> { it.isMultiSignal }.thenByDescending { it.hypeScore }.thenBy { it.startSec })
    }

    private fun finalizeClip(c: ClipCandidate, cues: List<TranscriptCue>, pad: PaddingPreset, dur: Double): ClipCandidate {
        val s = (c.startSec - pad.beforeSec).coerceAtLeast(0.0)
        val e = (c.endSec + pad.afterSec).coerceAtMost(dur).coerceAtLeast((s + 3.0).coerceAtMost(dur))
        return c.copy(startSec = s, endSec = e, transcriptQuote = SubtitleAndChatParser.extractQuoteAround(cues, s, e))
    }
}
''')

    w(f"{PKG}/engine/ClipExporter.kt", r'''
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
import com.yausername.youtubedl_android.YoutubeDL
import com.yausername.youtubedl_android.YoutubeDLRequest
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.nio.charset.StandardCharsets
import java.util.Locale

object ClipExporter {
    fun exportSingleClip(
        context: Context, sourceUrlOrUri: String, isLocalFile: Boolean, localFilePath: String?,
        videoTitle: String, clip: ClipCandidate, clipIndex: Int, exportMode: ExportMode, includeTxtNotes: Boolean
    ): Result<String> = runCatching {
        EngineInitializer.ensureInitialized(context).getOrThrow()
        val workDir = File(context.cacheDir, "export_${System.currentTimeMillis()}_$clipIndex").apply { mkdirs() }
        try {
            val safe = clip.title.replace(Regex("""[^a-zA-Z0-9._-]+"""), "_").trim('_').take(42).ifBlank { "Clip_${clipIndex + 1}" }
            val baseName = "ClipPulse_${clipIndex + 1}_$safe"
            val rawFile = File(workDir, "raw.mp4")
            val outMp4 = File(workDir, "$baseName.mp4")

            if (isLocalFile && !localFilePath.isNullOrBlank()) {
                val ss = TimeFormatter.formatFfmpegDuration(clip.startSec); val dur = TimeFormatter.formatFfmpegDuration(clip.durationSec)
                val args = if (exportMode == ExportMode.VERTICAL_CROP)
                    listOf("-y", "-ss", ss, "-i", localFilePath, "-t", dur, "-vf", "crop=ih*9/16:ih", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", outMp4.absolutePath)
                else listOf("-y", "-ss", ss, "-i", localFilePath, "-t", dur, "-c", "copy", "-movflags", "+faststart", outMp4.absolutePath)
                FfmpegRunner.run(context, args).getOrThrow()
            } else {
                val cleanUrl = UrlNormalizer.extractAndNormalize(sourceUrlOrUri)
                val req = YoutubeDLRequest(cleanUrl).apply {
                    addOption("-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]/bv*[height<=1080]+ba/b[height<=1080]/best")
                    addOption("--merge-output-format", "mp4")
                    addOption("--download-sections", "*${TimeFormatter.formatSectionTimestamp(clip.startSec)}-${TimeFormatter.formatSectionTimestamp(clip.endSec)}")
                    addOption("--force-keyframes-at-cuts"); addOption("--no-playlist"); addOption("-o", rawFile.absolutePath)
                }
                YoutubeDL.getInstance().execute(req)
                val dl = workDir.listFiles()?.firstOrNull { it.extension.equals("mp4", true) || it.name.startsWith("raw") }
                    ?: throw IllegalStateException("Section download produced no file.")
                val args = if (exportMode == ExportMode.VERTICAL_CROP)
                    listOf("-y", "-i", dl.absolutePath, "-vf", "crop=ih*9/16:ih", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", outMp4.absolutePath)
                else listOf("-y", "-i", dl.absolutePath, "-c", "copy", "-movflags", "+faststart", outMp4.absolutePath)
                FfmpegRunner.run(context, args).getOrThrow()
            }
            if (!outMp4.exists() || outMp4.length() == 0L) throw IllegalStateException("Rendered MP4 is empty.")
            val savedPath = saveVideo(context, outMp4, "$baseName.mp4")
            if (includeTxtNotes) saveTxt(context, "$baseName.txt", buildNotes(videoTitle, sourceUrlOrUri, clip, exportMode))
            savedPath
        } finally { workDir.deleteRecursively() }
    }

    private fun saveVideo(context: Context, src: File, name: String): String {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val r = context.contentResolver
            val v = ContentValues().apply {
                put(MediaStore.Video.Media.DISPLAY_NAME, name); put(MediaStore.Video.Media.MIME_TYPE, "video/mp4")
                put(MediaStore.Video.Media.RELATIVE_PATH, "${Environment.DIRECTORY_MOVIES}/ClipPulse"); put(MediaStore.Video.Media.IS_PENDING, 1)
            }
            val uri = r.insert(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, v) ?: throw IllegalStateException("MediaStore URI failed.")
            r.openOutputStream(uri)?.use { out -> FileInputStream(src).use { it.copyTo(out, 65536) } }
            v.clear(); v.put(MediaStore.Video.Media.IS_PENDING, 0); r.update(uri, v, null, null)
            return "Movies/ClipPulse/$name"
        }
        val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "ClipPulse").apply { mkdirs() }
        val dst = File(dir, name); FileInputStream(src).use { inp -> FileOutputStream(dst).use { inp.copyTo(it, 65536) } }
        MediaScannerConnection.scanFile(context, arrayOf(dst.absolutePath), arrayOf("video/mp4"), null)
        return dst.absolutePath
    }

    private fun saveTxt(context: Context, name: String, content: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val r = context.contentResolver
            val v = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, name); put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                put(MediaStore.MediaColumns.RELATIVE_PATH, "${Environment.DIRECTORY_DOCUMENTS}/ClipPulse"); put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
            val uri = r.insert(MediaStore.Files.getContentUri("external"), v) ?: return
            r.openOutputStream(uri)?.use { it.write(content.toByteArray(StandardCharsets.UTF_8)) }
            v.clear(); v.put(MediaStore.MediaColumns.IS_PENDING, 0); r.update(uri, v, null, null)
        } else {
            val dir = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS), "ClipPulse").apply { mkdirs() }
            File(dir, name).writeText(content, StandardCharsets.UTF_8)
        }
    }

    private fun buildNotes(videoTitle: String, url: String, clip: ClipCandidate, mode: ExportMode) = buildString {
        appendLine("ClipPulse Export Notes").appendLine("Title: ${clip.title}").appendLine("Source: $videoTitle ($url)")
        appendLine(String.format(Locale.US, "Range: %s - %s (%.1fs)", TimeFormatter.formatTimestamp(clip.startSec), TimeFormatter.formatTimestamp(clip.endSec), clip.durationSec))
        appendLine("Hype: ${clip.hypeScore}/100 | Mode: ${mode.label}")
        clip.superChat?.let { appendLine("Super Chat: ${it.donor} (${it.amountDisplay}) — ${it.message}") }
        if (clip.reason.isNotBlank()) appendLine("Signals: ${clip.reason}")
        if (clip.transcriptQuote.isNotBlank()) appendLine("Quote: \"${clip.transcriptQuote}\"")
    }
}
''')

    w(f"{PKG}/service/ClipExportService.kt", r'''
package com.clippulse.studio.service

import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.app.ServiceCompat
import androidx.core.content.ContextCompat
import com.clippulse.studio.engine.ClipExporter
import com.clippulse.studio.model.ClipCandidate
import com.clippulse.studio.model.ExportJobState
import com.clippulse.studio.model.ExportMode
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

object ExportProgressBus {
    private val _state = MutableStateFlow<ExportJobState>(ExportJobState.Idle)
    val state: StateFlow<ExportJobState> = _state.asStateFlow()
    @Volatile var pendingClips: List<ClipCandidate> = emptyList()
    fun update(s: ExportJobState) { _state.value = s }
    fun reset() { _state.value = ExportJobState.Idle }
}

class ClipExportService : Service() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    override fun onBind(intent: Intent?): IBinder? = null

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val url = intent?.getStringExtra("url").orEmpty()
        val isLocal = intent?.getBooleanExtra("local", false) ?: false
        val localPath = intent?.getStringExtra("path")
        val title = intent?.getStringExtra("title").orEmpty()
        val mode = runCatching { ExportMode.valueOf(intent?.getStringExtra("mode") ?: "") }.getOrDefault(ExportMode.FAST_COPY)
        val txt = intent?.getBooleanExtra("txt", true) ?: true
        val clips = ExportProgressBus.pendingClips

        val fgType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC else 0
        ServiceCompat.startForeground(this, 4102, buildNotif("ClipPulse Exporting", "Preparing ${clips.size} clip(s)...", 0, clips.size.coerceAtLeast(1), true), fgType)

        if (clips.isEmpty() || url.isBlank()) {
            ExportProgressBus.update(ExportJobState.Failed("No clips selected.")); stopSelf(); return START_NOT_STICKY
        }
        scope.launch {
            val saved = mutableListOf<String>(); var err: String? = null
            for ((i, c) in clips.withIndex()) {
                ExportProgressBus.update(ExportJobState.Running(i + 1, clips.size, c.title, i.toFloat() / clips.size))
                notifySafe(4102, "Exporting ${i + 1}/${clips.size}", c.title, i, clips.size, true)
                ClipExporter.exportSingleClip(applicationContext, url, isLocal, localPath, title, c, i, mode, txt)
                    .fold(onSuccess = { saved.add(it) }, onFailure = { err = it.message })
            }
            if (saved.isNotEmpty()) {
                ExportProgressBus.update(ExportJobState.Completed(saved.size, saved))
                notifySafe(4103, "Export Complete", "Saved ${saved.size} clip(s) to Movies/ClipPulse", 0, 0, false)
            } else {
                ExportProgressBus.update(ExportJobState.Failed(err ?: "Export failed"))
                notifySafe(4103, "Export Failed", err ?: "Export failed", 0, 0, false)
            }
            stopForeground(STOP_FOREGROUND_DETACH); stopSelf()
        }
        return START_NOT_STICKY
    }

    override fun onDestroy() { scope.cancel(); super.onDestroy() }

    private fun buildNotif(title: String, text: String, prog: Int, max: Int, ongoing: Boolean) =
        NotificationCompat.Builder(this, CHANNEL_ID).setSmallIcon(android.R.drawable.stat_sys_download)
            .setContentTitle(title).setContentText(text).setOnlyAlertOnce(true).setOngoing(ongoing)
            .apply { if (ongoing) setProgress(max, prog, false) else setAutoCancel(true) }.build()

    private fun notifySafe(id: Int, title: String, text: String, prog: Int, max: Int, ongoing: Boolean) {
        try { NotificationManagerCompat.from(this).notify(id, buildNotif(title, text, prog, max, ongoing)) } catch (_: SecurityException) {}
    }

    companion object {
        const val CHANNEL_ID = "clippulse_export_channel"
        fun startExport(ctx: Context, url: String, isLocal: Boolean, localPath: String?, title: String, clips: List<ClipCandidate>, mode: ExportMode, txt: Boolean) {
            ExportProgressBus.pendingClips = clips
            ContextCompat.startForegroundService(ctx, Intent(ctx, ClipExportService::class.java).apply {
                putExtra("url", url); putExtra("local", isLocal); putExtra("path", localPath)
                putExtra("title", title); putExtra("mode", mode.name); putExtra("txt", txt)
            })
        }
    }
}
''')



def write_ui_and_viewmodel() -> None:
    w(f"{PKG}/viewmodel/ClipPulseViewModel.kt", r'''
package com.clippulse.studio.viewmodel

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.engine.EngineInitializer
import com.clippulse.studio.engine.UrlNormalizer
import com.clippulse.studio.engine.VideoAnalysisEngine
import com.clippulse.studio.model.*
import com.clippulse.studio.network.UniversalAiClient
import com.clippulse.studio.service.ClipExportService
import com.clippulse.studio.service.ExportProgressBus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import kotlin.math.abs

data class StudioUiState(
    val sourceInput: String = "", val detectionMode: DetectionMode = DetectionMode.SMART_ALL,
    val customAiPrompt: String = "", val superChatThreshold: SuperChatThreshold = SuperChatThreshold.ALL,
    val paddingPreset: PaddingPreset = PaddingPreset.BALANCED, val isAnalyzing: Boolean = false,
    val analysisProgress: Float = 0f, val analysisStatus: String = "", val analysisError: String? = null,
    val analysisResult: VideoAnalysisResult? = null, val activeSignalFilter: SignalSource? = null,
    val expandedClipId: String? = null, val focusedClipId: String? = null,
    val exportMode: ExportMode = ExportMode.FAST_COPY, val includeTxtNotes: Boolean = true,
    val aiConfig: AiConfig = AiConfig(), val aiConnectionState: AiConnectionState = AiConnectionState.Idle,
    val isFetchingModels: Boolean = false, val modelFetchError: String? = null,
    val isAiSheetOpen: Boolean = false, val isUpdatingYtDlp: Boolean = false, val ytDlpUpdateStatus: String? = null
)

class ClipPulseViewModel(app: Application) : AndroidViewModel(app) {
    private val store = AiConfigStore(app)
    private val aiClient = UniversalAiClient()
    private val engine = VideoAnalysisEngine(aiClient)
    private val _ui = MutableStateFlow(StudioUiState(aiConfig = store.load()))
    val uiState: StateFlow<StudioUiState> = _ui.asStateFlow()
    val exportState: StateFlow<ExportJobState> = ExportProgressBus.state

    fun updateSourceInput(v: String) = _ui.update { it.copy(sourceInput = v, analysisError = null) }
    fun pasteAndNormalize(raw: String) {
        val clean = UrlNormalizer.extractAndNormalize(raw)
        if (clean.isNotBlank()) _ui.update { it.copy(sourceInput = clean, analysisError = null) }
    }
    fun onSharedUrlReceived(u: String) = _ui.update { it.copy(sourceInput = UrlNormalizer.extractAndNormalize(u), analysisError = null) }
    fun setDetectionMode(m: DetectionMode) = _ui.update { it.copy(detectionMode = m) }
    fun setCustomAiPrompt(p: String) = _ui.update { it.copy(customAiPrompt = p) }
    fun setSuperChatThreshold(t: SuperChatThreshold) = _ui.update { it.copy(superChatThreshold = t) }
    fun setPaddingPreset(p: PaddingPreset) = _ui.update { it.copy(paddingPreset = p) }
    fun setSignalFilter(s: SignalSource?) = _ui.update { it.copy(activeSignalFilter = s) }
    fun toggleClipExpanded(id: String) = _ui.update { it.copy(expandedClipId = if (it.expandedClipId == id) null else id) }
    fun setExportMode(m: ExportMode) = _ui.update { it.copy(exportMode = m) }
    fun toggleIncludeTxtNotes() = _ui.update { it.copy(includeTxtNotes = !it.includeTxtNotes) }
    fun dismissExportStatus() = ExportProgressBus.reset()
    fun setAiSheetOpen(open: Boolean) = _ui.update { it.copy(isAiSheetOpen = open) }

    fun focusClipAtTime(sec: Double) {
        val clips = _ui.value.analysisResult?.clips ?: return
        val nearest = clips.minByOrNull { abs(((it.startSec + it.endSec) / 2.0) - sec) } ?: return
        _ui.update { it.copy(focusedClipId = nearest.id, expandedClipId = nearest.id) }
    }

    fun toggleClipSelected(id: String) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        st.copy(analysisResult = r.copy(clips = r.clips.map { if (it.id == id) it.copy(selected = !it.selected) else it }))
    }

    fun selectAllClips(sel: Boolean) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        val f = st.activeSignalFilter
        st.copy(analysisResult = r.copy(clips = r.clips.map { if (f == null || f in it.signals) it.copy(selected = sel) else it }))
    }

    fun nudgeClipStart(id: String, delta: Double) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        st.copy(analysisResult = r.copy(clips = r.clips.map {
            if (it.id == id) it.copy(startSec = (it.startSec + delta).coerceIn(0.0, (it.endSec - 2.0).coerceAtLeast(0.0))) else it
        }))
    }

    fun nudgeClipEnd(id: String, delta: Double) = _ui.update { st ->
        val r = st.analysisResult ?: return@update st
        val maxD = r.durationSec.coerceAtLeast(1.0)
        st.copy(analysisResult = r.copy(clips = r.clips.map {
            if (it.id == id) it.copy(endSec = (it.endSec + delta).coerceIn((it.startSec + 2.0).coerceAtMost(maxD), maxD)) else it
        }))
    }

    fun analyzeRemoteUrl() {
        val normalized = UrlNormalizer.extractAndNormalize(_ui.value.sourceInput)
        if (normalized.isBlank()) { _ui.update { it.copy(analysisError = "Paste a YouTube or Facebook link first.") }; return }
        if (_ui.value.isAnalyzing) return
        viewModelScope.launch {
            _ui.update { it.copy(sourceInput = normalized, isAnalyzing = true, analysisProgress = 0.05f, analysisStatus = "Starting scan...", analysisError = null) }
            val s = _ui.value
            engine.analyzeRemoteUrl(getApplication(), normalized, s.detectionMode, s.superChatThreshold, s.paddingPreset, s.customAiPrompt, s.aiConfig) { p, msg ->
                _ui.update { it.copy(analysisProgress = p, analysisStatus = msg) }
            }.fold(
                onSuccess = { res -> _ui.update { it.copy(isAnalyzing = false, analysisProgress = 1f, analysisResult = res, activeSignalFilter = null, expandedClipId = res.clips.firstOrNull()?.id, focusedClipId = res.clips.firstOrNull()?.id) } },
                onFailure = { err -> _ui.update { it.copy(isAnalyzing = false, analysisError = err.message ?: "Analysis failed") } }
            )
        }
    }

    fun analyzeLocalVideoUri(uri: Uri) {
        if (_ui.value.isAnalyzing) return
        viewModelScope.launch {
            _ui.update { it.copy(sourceInput = uri.toString(), isAnalyzing = true, analysisProgress = 0.05f, analysisStatus = "Loading local video...", analysisError = null) }
            engine.analyzeLocalVideo(getApplication(), uri, _ui.value.paddingPreset) { p, msg ->
                _ui.update { it.copy(analysisProgress = p, analysisStatus = msg) }
            }.fold(
                onSuccess = { res -> _ui.update { it.copy(isAnalyzing = false, analysisProgress = 1f, analysisResult = res, activeSignalFilter = null, expandedClipId = res.clips.firstOrNull()?.id, focusedClipId = res.clips.firstOrNull()?.id) } },
                onFailure = { err -> _ui.update { it.copy(isAnalyzing = false, analysisError = err.message ?: "Local scan failed") } }
            )
        }
    }

    fun exportSelectedClips() {
        val s = _ui.value; val r = s.analysisResult ?: return
        val chosen = r.clips.filter { it.selected }
        if (chosen.isNotEmpty()) ClipExportService.startExport(getApplication(), r.sourceUrlOrUri, r.isLocalFile, r.localFilePath, r.videoTitle, chosen, s.exportMode, s.includeTxtNotes)
    }

    private fun saveCfg(fn: (AiConfig) -> AiConfig) = _ui.update { st -> val u = fn(st.aiConfig); store.save(u); st.copy(aiConfig = u, modelFetchError = null) }
    fun selectAiPreset(p: AiPreset) = saveCfg { it.copy(preset = p, baseUrl = p.defaultBaseUrl, selectedModel = p.defaultModel) }
    fun updateAiBaseUrl(u: String) = saveCfg { it.copy(baseUrl = u) }
    fun updatePrimaryApiKey(k: String) = saveCfg { it.copy(primaryKey = k) }
    fun addBackupApiKey(k: String) { if (k.isNotBlank()) saveCfg { it.copy(backupKeys = (it.backupKeys + k.trim()).distinct()) } }
    fun removeBackupApiKey(k: String) = saveCfg { it.copy(backupKeys = it.backupKeys.filterNot { x -> x == k }) }
    fun selectAiModel(m: String) = saveCfg { it.copy(selectedModel = m) }
    fun setSmartPeakOnly(e: Boolean) = saveCfg { it.copy(smartPeakOnly = e) }
    fun setOfflineNoAiMode(e: Boolean) = saveCfg { it.copy(offlineNoAiMode = e) }

    fun fetchAvailableModels() {
        val cfg = _ui.value.aiConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(_ui.value.aiConfig.baseUrl))
        store.save(cfg)
        viewModelScope.launch {
            _ui.update { it.copy(aiConfig = cfg, isFetchingModels = true, modelFetchError = null) }
            aiClient.fetchModels(cfg).fold(
                onSuccess = { models ->
                    val u = cfg.copy(availableModels = models, selectedModel = if (cfg.selectedModel in models) cfg.selectedModel else models.first())
                    store.save(u); _ui.update { it.copy(aiConfig = u, isFetchingModels = false) }
                },
                onFailure = { e -> _ui.update { it.copy(isFetchingModels = false, modelFetchError = e.message) } }
            )
        }
    }

    fun testAiConnection() {
        val cfg = _ui.value.aiConfig.copy(baseUrl = AiConfigStore.normalizeBaseUrl(_ui.value.aiConfig.baseUrl))
        store.save(cfg)
        viewModelScope.launch {
            _ui.update { it.copy(aiConfig = cfg, aiConnectionState = AiConnectionState.Testing) }
            _ui.update { it.copy(aiConnectionState = aiClient.testConnection(cfg)) }
        }
    }

    fun updateYtDlpBinary() {
        if (_ui.value.isUpdatingYtDlp) return
        viewModelScope.launch(Dispatchers.IO) {
            _ui.update { it.copy(isUpdatingYtDlp = true, ytDlpUpdateStatus = "Updating yt-dlp...") }
            EngineInitializer.updateYtDlpEngine(getApplication()).fold(
                onSuccess = { st -> _ui.update { it.copy(isUpdatingYtDlp = false, ytDlpUpdateStatus = "yt-dlp: $st") } },
                onFailure = { e -> _ui.update { it.copy(isUpdatingYtDlp = false, ytDlpUpdateStatus = "Error: ${e.message}") } }
            )
        }
    }
}
''')

    w(f"{PKG}/ui/theme/Theme.kt", r'''
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

@Composable
fun ClipPulseTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = ElectricIndigo, onPrimary = Color.White, secondary = ColorCyan,
            background = ObsidianBg, onBackground = TextPrimary, surface = MatteSlate,
            onSurface = TextPrimary, surfaceVariant = ElevatedSlate, onSurfaceVariant = TextSecondary,
            outline = HairlineBorder, error = ColorCrimson
        ),
        content = content
    )
}
''')

    w(f"{PKG}/ui/components/StudioComponents.kt", r'''
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui.components

import android.net.Uri
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import com.clippulse.studio.data.AiConfigStore
import com.clippulse.studio.model.*
import com.clippulse.studio.ui.theme.*
import java.io.File
import java.util.Locale

@Composable
fun ClipPulseLogo(modifier: Modifier = Modifier.size(34.dp)) {
    Canvas(modifier = modifier) {
        val w = size.width; val h = size.height
        drawRoundRect(MatteSlate, size = Size(w, h), cornerRadius = CornerRadius(w * 0.24f, h * 0.24f))
        drawRoundRect(Brush.linearGradient(listOf(ElectricIndigo, ColorCyan)), size = Size(w, h), cornerRadius = CornerRadius(w * 0.24f, h * 0.24f), style = Stroke(w * 0.06f))
        val p = Path().apply {
            moveTo(w * 0.16f, h * 0.54f); lineTo(w * 0.30f, h * 0.54f); lineTo(w * 0.39f, h * 0.28f)
            lineTo(w * 0.50f, h * 0.76f); lineTo(w * 0.61f, h * 0.34f); lineTo(w * 0.70f, h * 0.58f); lineTo(w * 0.84f, h * 0.54f)
        }
        drawPath(p, Brush.horizontalGradient(listOf(ElectricIndigo, ColorCyan)), style = Stroke(w * 0.085f, cap = StrokeCap.Round, join = StrokeJoin.Round))
        drawCircle(ColorGold, radius = w * 0.08f, center = Offset(w * 0.78f, h * 0.24f))
    }
}

@Composable
fun InteractiveHeatmapTimeline(durationSec: Double, heatmap: List<HeatmapPoint>, clips: List<ClipCandidate>, focusedClipId: String?, onJumpToTime: (Double) -> Unit) {
    val safeDur = durationSec.coerceAtLeast(1.0)
    Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(1.dp, HairlineBorder)) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("REPLAY HEATMAP & TIMELINE", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                Text("Tap to jump", color = TextMuted, fontSize = 11.sp)
            }
            Spacer(Modifier.height(8.dp))
            Canvas(modifier = Modifier.fillMaxWidth().height(82.dp)
                .pointerInput(safeDur, clips) { detectTapGestures { onJumpToTime((it.x / size.width).coerceIn(0f, 1f) * safeDur) } }
                .pointerInput(safeDur, clips) { detectHorizontalDragGestures { ch, _ -> onJumpToTime((ch.position.x / size.width).coerceIn(0f, 1f) * safeDur) } }
            ) {
                val w = size.width; val h = size.height
                drawRoundRect(ElevatedSlate, size = Size(w, h))
                if (heatmap.size >= 2) {
                    val line = Path(); val fill = Path()
                    heatmap.forEachIndexed { i, pt ->
                        val x = (((pt.startSec + pt.endSec) / 2.0 / safeDur).toFloat().coerceIn(0f, 1f)) * w
                        val y = h - (pt.value.toFloat().coerceIn(0.05f, 1f) * (h * 0.82f)) - (h * 0.06f)
                        if (i == 0) { line.moveTo(0f, y); fill.moveTo(0f, h); fill.lineTo(0f, y) }
                        line.lineTo(x, y); fill.lineTo(x, y)
                        if (i == heatmap.lastIndex) { line.lineTo(w, y); fill.lineTo(w, y); fill.lineTo(w, h); fill.close() }
                    }
                    drawPath(fill, Brush.verticalGradient(listOf(ColorCrimson.copy(alpha = 0.34f), ElectricIndigo.copy(alpha = 0.06f))))
                    drawPath(line, Brush.horizontalGradient(listOf(ElectricIndigo, ColorCrimson, ColorGold)), style = Stroke(2.2.dp.toPx(), cap = StrokeCap.Round))
                }
                for (c in clips) {
                    val sx = ((c.startSec / safeDur).toFloat().coerceIn(0f, 1f)) * w
                    val ex = ((c.endSec / safeDur).toFloat().coerceIn(0f, 1f)) * w
                    val col = if (c.isMultiSignal) ColorGold else c.signals.firstOrNull()?.badgeColor ?: ElectricIndigo
                    val foc = c.id == focusedClipId
                    drawRect(col.copy(alpha = if (foc) 0.34f else 0.16f), topLeft = Offset(sx, 0f), size = Size((ex - sx).coerceAtLeast(3.dp.toPx()), h))
                    drawLine(if (foc) TextPrimary else col, Offset(sx, 0f), Offset(sx, h), strokeWidth = if (foc) 2.5.dp.toPx() else 1.5.dp.toPx())
                }
            }
            Spacer(Modifier.height(4.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("00:00", color = TextMuted, fontSize = 11.sp)
                Text(TimeFormatter.formatTimestamp(safeDur / 2.0), color = TextMuted, fontSize = 11.sp)
                Text(TimeFormatter.formatTimestamp(safeDur), color = TextMuted, fontSize = 11.sp)
            }
        }
    }
}

@Composable
fun ClipPreviewPlayer(localFilePath: String, startSec: Double, endSec: Double) {
    val ctx = LocalContext.current
    var playing by remember { mutableStateOf(false) }
    val player = remember(localFilePath) {
        ExoPlayer.Builder(ctx).build().apply {
            setMediaItem(MediaItem.fromUri(Uri.fromFile(File(localFilePath))))
            prepare(); seekTo((startSec * 1000.0).toLong())
        }
    }
    LaunchedEffect(startSec) { player.seekTo((startSec * 1000.0).toLong()) }
    DisposableEffect(player) {
        val l = object : Player.Listener { override fun onIsPlayingChanged(p: Boolean) { playing = p } }
        player.addListener(l)
        onDispose { player.removeListener(l); player.release() }
    }
    Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
        Column(Modifier.padding(8.dp)) {
            AndroidView(factory = { c -> PlayerView(c).apply { this.player = player; useController = false } }, modifier = Modifier.fillMaxWidth().height(160.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row {
                    IconButton(onClick = { if (player.isPlaying) player.pause() else { if (player.currentPosition >= (endSec * 1000.0).toLong()) player.seekTo((startSec * 1000.0).toLong()); player.play() } }) {
                        Icon(if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow, "Play", tint = ElectricIndigoLight)
                    }
                    IconButton(onClick = { player.seekTo((startSec * 1000.0).toLong()); player.play() }) {
                        Icon(Icons.Rounded.Refresh, "Replay", tint = TextSecondary)
                    }
                }
                Text("${TimeFormatter.formatTimestamp(startSec)} - ${TimeFormatter.formatTimestamp(endSec)}", color = TextSecondary, fontSize = 11.sp)
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ClipCard(
    clip: ClipCandidate, isExpanded: Boolean, isFocused: Boolean, localVideoPath: String?,
    onToggleSelect: () -> Unit, onToggleExpand: () -> Unit, onNudgeStart: (Double) -> Unit, onNudgeEnd: (Double) -> Unit
) {
    val border = when { isFocused -> ElectricIndigo; clip.isMultiSignal -> ColorGold.copy(alpha = 0.55f); else -> HairlineBorder }
    Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(16.dp), border = BorderStroke(if (isFocused) 1.5.dp else 1.dp, border)) {
        Column(Modifier.padding(12.dp)) {
            Row(modifier = Modifier.fillMaxWidth().clickable { onToggleExpand() }, verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = clip.selected, onCheckedChange = { onToggleSelect() }, colors = CheckboxDefaults.colors(checkedColor = ElectricIndigo))
                Column(Modifier.weight(1f)) {
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        if (clip.isMultiSignal) BadgePill("\uD83D\uDD25 Multi-Signal", ColorGold)
                        clip.signals.forEach { BadgePill(it.label, it.badgeColor) }
                    }
                    Spacer(Modifier.height(5.dp))
                    Text(clip.title, color = TextPrimary, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    Text(String.format(Locale.US, "%s - %s • %.1fs", TimeFormatter.formatTimestamp(clip.startSec), TimeFormatter.formatTimestamp(clip.endSec), clip.durationSec), color = ElectricIndigoLight, fontSize = 12.sp)
                }
                Column(horizontalAlignment = Alignment.End) {
                    val hc = when { clip.hypeScore >= 88 -> ColorGold; clip.hypeScore >= 76 -> ColorEmerald; else -> ElectricIndigoLight }
                    Surface(color = hc.copy(alpha = 0.16f), shape = RoundedCornerShape(10.dp), border = BorderStroke(1.dp, hc.copy(alpha = 0.45f))) {
                        Column(Modifier.padding(horizontal = 9.dp, vertical = 4.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("${clip.hypeScore}", color = hc, fontSize = 15.sp, fontWeight = FontWeight.Bold)
                            Text("HYPE", color = hc, fontSize = 9.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }
                    Icon(if (isExpanded) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore, "Expand", tint = TextSecondary)
                }
            }
            clip.superChat?.let { sc ->
                Spacer(Modifier.height(8.dp))
                Surface(modifier = Modifier.fillMaxWidth(), color = ColorGold.copy(alpha = 0.12f), shape = RoundedCornerShape(10.dp), border = BorderStroke(1.dp, ColorGold.copy(alpha = 0.4f))) {
                    Row(Modifier.padding(9.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Rounded.Paid, "Super Chat", tint = ColorGold, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(8.dp))
                        Column {
                            Text("${sc.donor} • ${sc.amountDisplay}", color = ColorGold, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            if (sc.message.isNotBlank()) Text(sc.message, color = TextPrimary, fontSize = 12.sp)
                        }
                    }
                }
            }
            if (clip.transcriptQuote.isNotBlank()) {
                Spacer(Modifier.height(6.dp))
                Text("\"${clip.transcriptQuote}\"", color = TextSecondary, fontSize = 12.sp, fontStyle = FontStyle.Italic, maxLines = if (isExpanded) 5 else 2, overflow = TextOverflow.Ellipsis)
            }
            AnimatedVisibility(visible = isExpanded) {
                Column(Modifier.padding(top = 10.dp)) {
                    HorizontalDivider(color = HairlineBorder); Spacer(Modifier.height(8.dp))
                    if (clip.reason.isNotBlank()) { Text(clip.reason, color = TextSecondary, fontSize = 12.sp); Spacer(Modifier.height(8.dp)) }
                    if (!localVideoPath.isNullOrBlank()) { ClipPreviewPlayer(localVideoPath, clip.startSec, clip.endSec); Spacer(Modifier.height(8.dp)) }
                    Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                        Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Start: ${TimeFormatter.formatTimestamp(clip.startSec)}", color = TextPrimary, fontSize = 12.sp)
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeBtn("-2s") { onNudgeStart(-2.0) }; NudgeBtn("+2s") { onNudgeStart(2.0) }
                                }
                            }
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("End: ${TimeFormatter.formatTimestamp(clip.endSec)}", color = TextPrimary, fontSize = 12.sp)
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    NudgeBtn("-2s") { onNudgeEnd(-2.0) }; NudgeBtn("+2s") { onNudgeEnd(2.0) }
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
private fun BadgePill(label: String, c: Color) {
    Surface(color = c.copy(alpha = 0.16f), shape = RoundedCornerShape(6.dp), border = BorderStroke(1.dp, c.copy(alpha = 0.45f))) {
        Text(label, color = c, fontSize = 10.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp))
    }
}

@Composable
private fun NudgeBtn(label: String, onClick: () -> Unit) {
    OutlinedButton(onClick = onClick, shape = RoundedCornerShape(8.dp), border = BorderStroke(1.dp, HairlineBorder), contentPadding = PaddingValues(horizontal = 10.dp, vertical = 2.dp), modifier = Modifier.height(28.dp)) {
        Text(label, color = ElectricIndigoLight, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun AiManagerSheet(
    config: AiConfig, connectionState: AiConnectionState, isFetchingModels: Boolean, modelFetchError: String?,
    isUpdatingYtDlp: Boolean, ytDlpUpdateStatus: String?, onDismiss: () -> Unit, onSelectPreset: (AiPreset) -> Unit,
    onUpdateBaseUrl: (String) -> Unit, onUpdatePrimaryKey: (String) -> Unit, onAddBackupKey: (String) -> Unit,
    onRemoveBackupKey: (String) -> Unit, onSelectModel: (String) -> Unit, onFetchModels: () -> Unit,
    onTestConnect: () -> Unit, onToggleSmartPeakOnly: (Boolean) -> Unit, onToggleOfflineMode: (Boolean) -> Unit, onUpdateYtDlp: () -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var showKey by remember { mutableStateOf(false) }
    var backupInput by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }
    var filter by remember { mutableStateOf("") }

    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = sheetState, containerColor = MatteSlate, contentColor = TextPrimary) {
        Column(modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 18.dp, vertical = 8.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Universal AI API & Engine Manager", color = TextPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                AiPreset.entries.forEach { p ->
                    FilterChip(selected = config.preset == p, onClick = { onSelectPreset(p) }, label = { Text(p.displayName, fontSize = 12.sp) })
                }
            }
            OutlinedTextField(value = config.baseUrl, onValueChange = onUpdateBaseUrl, label = { Text("Base URL") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            Text("Normalized: ${AiConfigStore.normalizeBaseUrl(config.baseUrl)}", color = TextMuted, fontSize = 11.sp)
            OutlinedTextField(
                value = config.primaryKey, onValueChange = onUpdatePrimaryKey, label = { Text("Primary API Key") }, singleLine = true,
                visualTransformation = if (showKey) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = { IconButton(onClick = { showKey = !showKey }) { Icon(if (showKey) Icons.Rounded.VisibilityOff else Icons.Rounded.Visibility, "Show") } },
                modifier = Modifier.fillMaxWidth()
            )
            Surface(modifier = Modifier.fillMaxWidth(), color = ElevatedSlate, shape = RoundedCornerShape(12.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                Column(Modifier.padding(10.dp)) {
                    Text("BACKUP FAILOVER KEYS (${config.backupKeys.size})", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                    Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                        OutlinedTextField(value = backupInput, onValueChange = { backupInput = it }, placeholder = { Text("Add backup key", fontSize = 12.sp) }, singleLine = true, modifier = Modifier.weight(1f))
                        IconButton(onClick = { onAddBackupKey(backupInput); backupInput = "" }) { Icon(Icons.Rounded.Add, "Add", tint = ElectricIndigoLight) }
                    }
                    config.backupKeys.forEachIndexed { idx, k ->
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Key #${idx + 1}: ${if (k.length > 10) "${k.take(6)}••••${k.takeLast(4)}" else "••••"}", color = TextPrimary, fontSize = 12.sp)
                            IconButton(onClick = { onRemoveBackupKey(k) }, modifier = Modifier.size(28.dp)) { Icon(Icons.Rounded.Delete, "Del", tint = ColorCrimson, modifier = Modifier.size(16.dp)) }
                        }
                    }
                }
            }
            ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                OutlinedTextField(
                    value = config.selectedModel, onValueChange = { onSelectModel(it); filter = it }, label = { Text("Model ID") }, singleLine = true,
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                    modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryEditable, enabled = true).fillMaxWidth()
                )
                val matches = config.availableModels.filter { filter.isBlank() || it.contains(filter, ignoreCase = true) }
                ExposedDropdownMenu(expanded = expanded && matches.isNotEmpty(), onDismissRequest = { expanded = false }, modifier = Modifier.heightIn(max = 200.dp)) {
                    matches.forEach { id -> DropdownMenuItem(text = { Text(id, fontSize = 13.sp) }, onClick = { onSelectModel(id); filter = ""; expanded = false }) }
                }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedButton(onClick = onFetchModels, enabled = !isFetchingModels, modifier = Modifier.weight(1f)) {
                    if (isFetchingModels) CircularProgressIndicator(Modifier.size(16.dp), strokeWidth = 2.dp) else Icon(Icons.Rounded.Refresh, "Fetch", Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp)); Text("Fetch Models", fontSize = 12.sp)
                }
                Button(onClick = onTestConnect, enabled = connectionState !is AiConnectionState.Testing, colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), modifier = Modifier.weight(1f)) {
                    if (connectionState is AiConnectionState.Testing) CircularProgressIndicator(color = TextPrimary, modifier = Modifier.size(16.dp), strokeWidth = 2.dp) else Icon(Icons.Rounded.Bolt, "Connect", Modifier.size(16.dp))
                    Spacer(Modifier.width(6.dp)); Text("Connect", fontSize = 12.sp)
                }
            }
            if (modelFetchError != null) Text(modelFetchError, color = ColorCrimson, fontSize = 12.sp)
            when (connectionState) {
                is AiConnectionState.Connected -> Text("\u2713 Connected (${connectionState.latencyMs} ms) • ${connectionState.model}", color = ColorEmerald, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                is AiConnectionState.Error -> Text(connectionState.message, color = ColorCrimson, fontSize = 12.sp)
                else -> Unit
            }
            HorizontalDivider(color = HairlineBorder)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Smart Peak-Only Mode (~85% token savings)", color = TextPrimary, fontSize = 13.sp, modifier = Modifier.weight(1f))
                Switch(checked = config.smartPeakOnly, onCheckedChange = onToggleSmartPeakOnly)
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("100% Offline / No-AI Mode", color = TextPrimary, fontSize = 13.sp, modifier = Modifier.weight(1f))
                Switch(checked = config.offlineNoAiMode, onCheckedChange = onToggleOfflineMode)
            }
            OutlinedButton(onClick = onUpdateYtDlp, enabled = !isUpdatingYtDlp, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.Update, "Update", Modifier.size(16.dp)); Spacer(Modifier.width(8.dp))
                Text("Update yt-dlp Extractor Engine", fontSize = 12.sp)
            }
            if (ytDlpUpdateStatus != null) Text(ytDlpUpdateStatus, color = ElectricIndigoLight, fontSize = 12.sp)
            Spacer(Modifier.height(16.dp))
        }
    }
}
''')

    w(f"{PKG}/ui/ClipPulseStudioScreen.kt", r'''
@file:OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)

package com.clippulse.studio.ui

import android.Manifest
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
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
import com.clippulse.studio.model.*
import com.clippulse.studio.ui.components.*
import com.clippulse.studio.ui.theme.*
import com.clippulse.studio.viewmodel.ClipPulseViewModel

@Composable
fun ClipPulseStudioScreen(viewModel: ClipPulseViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val exportState by viewModel.exportState.collectAsStateWithLifecycle()
    val clipboard = LocalClipboardManager.current
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri -> if (uri != null) viewModel.analyzeLocalVideoUri(uri) }
    val notifPerm = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { viewModel.exportSelectedClips() }

    val res = state.analysisResult
    val visible = res?.clips?.filter { state.activeSignalFilter == null || state.activeSignalFilter in it.signals }.orEmpty()
    val selectedCount = res?.clips?.count { it.selected } ?: 0

    Scaffold(
        containerColor = ObsidianBg,
        topBar = {
            Surface(color = ObsidianBg, modifier = Modifier.fillMaxWidth().statusBarsPadding()) {
                Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        ClipPulseLogo(); Spacer(Modifier.width(10.dp))
                        Column {
                            Text("ClipPulse", color = TextPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            Text("Zero-Download Clip Studio", color = TextMuted, fontSize = 11.sp)
                        }
                    }
                    val (pillTxt, pillCol) = when {
                        state.aiConfig.offlineNoAiMode -> "Offline Mode" to TextSecondary
                        state.aiConnectionState is AiConnectionState.Connected -> "\u2713 ${(state.aiConnectionState as AiConnectionState.Connected).latencyMs}ms" to ColorEmerald
                        state.aiConnectionState is AiConnectionState.Error -> "AI Error" to ColorCrimson
                        state.aiConfig.primaryKey.isNotBlank() -> state.aiConfig.preset.displayName to ElectricIndigoLight
                        else -> "Setup AI" to ColorGold
                    }
                    Surface(onClick = { viewModel.setAiSheetOpen(true) }, color = pillCol.copy(alpha = 0.14f), shape = RoundedCornerShape(20.dp), border = BorderStroke(1.dp, pillCol.copy(alpha = 0.45f))) {
                        Text(pillTxt, color = pillCol, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp))
                    }
                }
            }
        },
        bottomBar = {
            if (res != null) {
                Surface(color = MatteSlate, border = BorderStroke(1.dp, HairlineBorder), modifier = Modifier.fillMaxWidth().navigationBarsPadding()) {
                    Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        when (val es = exportState) {
                            is ExportJobState.Running -> {
                                LinearProgressIndicator(progress = { es.progressFraction }, color = ElectricIndigo, modifier = Modifier.fillMaxWidth())
                                Text("Exporting ${es.currentIndex}/${es.total}: ${es.currentTitle}", color = ElectricIndigoLight, fontSize = 12.sp, maxLines = 1)
                            }
                            is ExportJobState.Completed -> Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("Saved ${es.exportedCount} clip(s) to Movies/ClipPulse", color = ColorEmerald, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                                TextButton(onClick = viewModel::dismissExportStatus) { Text("OK", color = ColorEmerald, fontSize = 12.sp) }
                            }
                            is ExportJobState.Failed -> Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text(es.error, color = ColorCrimson, fontSize = 12.sp, modifier = Modifier.weight(1f))
                                TextButton(onClick = viewModel::dismissExportStatus) { Text("Dismiss", color = ColorCrimson, fontSize = 12.sp) }
                            }
                            ExportJobState.Idle -> Unit
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            FilterChip(selected = state.exportMode == ExportMode.FAST_COPY, onClick = { viewModel.setExportMode(ExportMode.FAST_COPY) }, label = { Text("Fast Cut", fontSize = 11.sp) })
                            FilterChip(selected = state.exportMode == ExportMode.VERTICAL_CROP, onClick = { viewModel.setExportMode(ExportMode.VERTICAL_CROP) }, label = { Text("9:16 Crop", fontSize = 11.sp) })
                            FilterChip(selected = state.includeTxtNotes, onClick = viewModel::toggleIncludeTxtNotes, label = { Text("+.TXT", fontSize = 11.sp) })
                        }
                        Button(
                            onClick = { if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) notifPerm.launch(Manifest.permission.POST_NOTIFICATIONS) else viewModel.exportSelectedClips() },
                            enabled = selectedCount > 0 && exportState !is ExportJobState.Running,
                            colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.fillMaxWidth().height(46.dp)
                        ) {
                            Icon(Icons.Rounded.FileDownload, "Export", Modifier.size(18.dp)); Spacer(Modifier.width(8.dp))
                            Text("Export Selected Clips to Gallery ($selectedCount)", fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                        }
                    }
                }
            }
        }
    ) { pad ->
        LazyColumn(modifier = Modifier.fillMaxSize().padding(pad), contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            item {
                Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(18.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                    Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        OutlinedTextField(value = state.sourceInput, onValueChange = viewModel::updateSourceInput, placeholder = { Text("YouTube URL, Live VOD, or Facebook Video...", fontSize = 13.sp) }, singleLine = true, modifier = Modifier.fillMaxWidth())
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            OutlinedButton(onClick = { clipboard.getText()?.text?.let(viewModel::pasteAndNormalize) }, modifier = Modifier.weight(1f)) {
                                Icon(Icons.Rounded.ContentPaste, "Paste", Modifier.size(16.dp)); Spacer(Modifier.width(6.dp)); Text("Paste Link", fontSize = 12.sp)
                            }
                            OutlinedButton(onClick = { picker.launch("video/*") }, modifier = Modifier.weight(1f)) {
                                Icon(Icons.Rounded.VideoLibrary, "Local", Modifier.size(16.dp)); Spacer(Modifier.width(6.dp)); Text("Local Video", fontSize = 12.sp)
                            }
                        }
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            DetectionMode.entries.forEach { m -> FilterChip(selected = state.detectionMode == m, onClick = { viewModel.setDetectionMode(m) }, label = { Text(m.label, fontSize = 11.sp) }) }
                        }
                        if (state.detectionMode == DetectionMode.AI_CUSTOM || state.detectionMode == DetectionMode.SMART_ALL) {
                            OutlinedTextField(value = state.customAiPrompt, onValueChange = viewModel::setCustomAiPrompt, placeholder = { Text("Optional AI prompt (e.g., \"every rage moment\")", fontSize = 12.sp) }, singleLine = true, modifier = Modifier.fillMaxWidth())
                        }
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Text("Super Chat:", color = TextMuted, fontSize = 11.sp)
                            SuperChatThreshold.entries.forEach { t -> FilterChip(selected = state.superChatThreshold == t, onClick = { viewModel.setSuperChatThreshold(t) }, label = { Text(t.label, fontSize = 11.sp) }) }
                        }
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Text("Padding:", color = TextMuted, fontSize = 11.sp)
                            PaddingPreset.entries.forEach { p -> FilterChip(selected = state.paddingPreset == p, onClick = { viewModel.setPaddingPreset(p) }, label = { Text(p.label, fontSize = 11.sp) }) }
                        }
                        Button(onClick = viewModel::analyzeRemoteUrl, enabled = !state.isAnalyzing, colors = ButtonDefaults.buttonColors(containerColor = ElectricIndigo), shape = RoundedCornerShape(12.dp), modifier = Modifier.fillMaxWidth().height(46.dp)) {
                            if (state.isAnalyzing) { CircularProgressIndicator(color = TextPrimary, modifier = Modifier.size(18.dp), strokeWidth = 2.dp); Spacer(Modifier.width(8.dp)); Text("Scanning Signals...") }
                            else { Icon(Icons.Rounded.AutoAwesome, "Analyze", Modifier.size(18.dp)); Spacer(Modifier.width(8.dp)); Text("Analyze Video (Zero-Download)", fontWeight = FontWeight.SemiBold) }
                        }
                        if (state.isAnalyzing) {
                            LinearProgressIndicator(progress = { state.analysisProgress }, color = ElectricIndigo, modifier = Modifier.fillMaxWidth())
                            Text(state.analysisStatus, color = ElectricIndigoLight, fontSize = 12.sp)
                        }
                        if (state.analysisError != null) Text(state.analysisError.orEmpty(), color = ColorCrimson, fontSize = 12.sp)
                    }
                }
            }
            if (res != null) {
                item {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Surface(modifier = Modifier.fillMaxWidth(), color = MatteSlate, shape = RoundedCornerShape(14.dp), border = BorderStroke(1.dp, HairlineBorder)) {
                            Column(Modifier.padding(12.dp)) {
                                Text(res.videoTitle, color = TextPrimary, fontSize = 15.sp, fontWeight = FontWeight.Bold, maxLines = 2, overflow = TextOverflow.Ellipsis)
                                Text("${res.channelName} • ${res.analysisSummary}", color = TextSecondary, fontSize = 12.sp)
                            }
                        }
                        InteractiveHeatmapTimeline(res.durationSec, res.heatmap, res.clips, state.focusedClipId, viewModel::focusClipAtTime)
                        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            FilterChip(selected = state.activeSignalFilter == null, onClick = { viewModel.setSignalFilter(null) }, label = { Text("All (${res.clips.size})", fontSize = 11.sp) })
                            SignalSource.entries.forEach { sig ->
                                val cnt = res.clips.count { sig in it.signals }
                                if (cnt > 0) FilterChip(selected = state.activeSignalFilter == sig, onClick = { viewModel.setSignalFilter(if (state.activeSignalFilter == sig) null else sig) }, label = { Text("${sig.label} ($cnt)", fontSize = 11.sp) })
                            }
                        }
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("DETECTED CLIPS ($selectedCount/${res.clips.size})", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                            Row {
                                TextButton(onClick = { viewModel.selectAllClips(true) }) { Text("Select All", color = ElectricIndigoLight, fontSize = 12.sp) }
                                TextButton(onClick = { viewModel.selectAllClips(false) }) { Text("Clear", color = TextSecondary, fontSize = 12.sp) }
                            }
                        }
                    }
                }
                items(items = visible, key = { it.id }) { clip ->
                    ClipCard(clip, state.expandedClipId == clip.id, state.focusedClipId == clip.id, res.localFilePath,
                        { viewModel.toggleClipSelected(clip.id) }, { viewModel.toggleClipExpanded(clip.id) },
                        { viewModel.nudgeClipStart(clip.id, it) }, { viewModel.nudgeClipEnd(clip.id, it) })
                }
            }
        }
    }

    if (state.isAiSheetOpen) {
        AiManagerSheet(
            state.aiConfig, state.aiConnectionState, state.isFetchingModels, state.modelFetchError,
            state.isUpdatingYtDlp, state.ytDlpUpdateStatus, { viewModel.setAiSheetOpen(false) }, viewModel::selectAiPreset,
            viewModel::updateAiBaseUrl, viewModel::updatePrimaryApiKey, viewModel::addBackupApiKey, viewModel::removeBackupApiKey,
            viewModel::selectAiModel, viewModel::fetchAvailableModels, viewModel::testAiConnection,
            viewModel::setSmartPeakOnly, viewModel::setOfflineNoAiMode, viewModel::updateYtDlpBinary
        )
    }
}
''')


def main() -> None:
    write_gradle_and_manifest()
    write_core_kotlin()
    write_engines_and_service()
    write_ui_and_viewmodel()
    print("\nClipPulse Android project generated successfully!")


if __name__ == "__main__":
    main()
    sys.exit(0)
