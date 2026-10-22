plugins {
    id("com.android.application")
}

// Version : la CI passe le numéro de build et le nom du tag (apk-v1.2 → 1.2).
val codeVersion = (System.getenv("QCM_VERSION_CODE") ?: "1").toInt()
val nomVersion = System.getenv("QCM_VERSION_NAME") ?: "dev"

// Signature : clé privée fournie par la CI (secrets GitHub) si elle existe,
// sinon la clé du dépôt (android/signature/), pour que chaque release puisse
// s'installer par-dessus la précédente sans perdre les réponses gardées.
val cleSignature = System.getenv("QCM_KEYSTORE")?.let { file(it) } ?: rootProject.file("signature/qcm.jks")

val katexVersion = "0.16.47"
val webGenere = layout.buildDirectory.dir("generated/web")

android {
    namespace = "fr.projetpluri.qcm"
    compileSdk = 35

    defaultConfig {
        applicationId = "fr.projetpluri.qcm"
        minSdk = 26
        targetSdk = 35
        versionCode = codeVersion
        versionName = nomVersion
    }

    signingConfigs {
        create("release") {
            storeFile = cleSignature
            storePassword = System.getenv("QCM_KEYSTORE_PASSWORD") ?: "projetpluri"
            keyAlias = System.getenv("QCM_KEY_ALIAS") ?: "qcm"
            keyPassword = System.getenv("QCM_KEY_PASSWORD") ?: "projetpluri"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("release")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    sourceSets["main"].assets.srcDir(webGenere)

    lint {
        checkReleaseBuilds = false
    }
}

dependencies {
    implementation("androidx.webkit:webkit:1.13.0")
}

// Le moteur des QCM est celui du wiki (wiki/static/wiki/) : copié à chaque build,
// avec KaTeX (paquet npm, même version que le CDN du site) pour les formules hors ligne.
val telechargerKatex by tasks.registering {
    val archive = layout.buildDirectory.file("katex-$katexVersion.tgz")
    outputs.file(archive)
    doLast {
        val cible = archive.get().asFile
        if (!cible.exists()) {
            cible.parentFile.mkdirs()
            uri("https://registry.npmjs.org/katex/-/katex-$katexVersion.tgz").toURL().openStream().use { entree ->
                cible.outputStream().use { entree.copyTo(it) }
            }
        }
    }
}

val preparerWeb by tasks.registering(Sync::class) {
    dependsOn(telechargerKatex)
    into(webGenere)
    from(rootProject.file("../wiki/static/wiki")) {
        include("quiz.js", "qcm_attente.js", "qcm_hors_ligne.js", "wiki.css")
        into("web")
    }
    from(tarTree(resources.gzip(layout.buildDirectory.file("katex-$katexVersion.tgz")))) {
        include("package/dist/katex.min.css", "package/dist/katex.min.js", "package/dist/fonts/*.woff2")
        eachFile { path = path.replaceFirst("package/", "lib/katex@$katexVersion/") }
        includeEmptyDirs = false
    }
}

tasks.named("preBuild") { dependsOn(preparerWeb) }
