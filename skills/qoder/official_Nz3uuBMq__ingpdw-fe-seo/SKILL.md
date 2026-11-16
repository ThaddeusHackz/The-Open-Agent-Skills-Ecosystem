---
name: fe-seo
description: Next.js 앱의 SEO와 메타데이터를 최적화하는 스킬. Metadata API, Open Graph, JSON-LD 구조화 데이터, sitemap, robots.txt, 동적 OG 이미지 등. "SEO", "메타데이터", "metadata", "OG", "오픈그래프", "사이트맵", "검색 최적화" 등의 요청 시 사용.
argument-hint: "[파일경로 또는 키워드] (예: src/app/page.tsx, sitemap, og-image)"
---

# FE SEO & Metadata Optimization

`$ARGUMENTS`를 분석하여 SEO 관련 메타데이터를 최적화하거나 생성한다.

## 분석 절차

1. **현재 상태 파악**: 프로젝트의 메타데이터 설정을 Glob/Read로 확인한다
2. **SEO 체크리스트 검사**: 아래 항목에 대해 누락 사항을 확인한다
3. **개선안 제시**: 구체적인 코드와 함께 최적화 방안을 제시한다
4. **구현**: 승인 후 메타데이터를 추가/수정한다

## Next.js Metadata API

### 정적 Metadata

```tsx
// src/app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  metadataBase: new URL("https://example.com"),
  title: {
    default: "사이트명",
    template: "%s | 사이트명",  // 하위 페이지에서 title만 지정하면 자동 조합
  },
  description: "사이트 설명 (155자 이내 권장)",
  keywords: ["키워드1", "키워드2", "키워드3"],
  authors: [{ name: "작성자명" }],
  creator: "회사명",
  openGraph: {
    type: "website",
    locale: "ko_KR",
    url: "https://example.com",
    siteName: "사이트명",
    title: "사이트명",
    description: "사이트 설명",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "사이트명 대표 이미지",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "사이트명",
    description: "사이트 설명",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "google-verification-code",
    naver: "naver-verification-code",
  },
};
```

### 동적 Metadata (페이지별)

```tsx
// src/app/blog/[slug]/page.tsx
import type { Metadata } from "next";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) {
    return { title: "포스트를 찾을 수 없습니다" };
  }

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      publishedTime: post.publishedAt,
      authors: [post.author.name],
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}

export default async function BlogPostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);
  // ...
}
```

## JSON-LD 구조화 데이터

### 웹사이트 (조직)

```tsx
// src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "회사명",
    url: "https://example.com",
    logo: "https://example.com/logo.png",
    sameAs: [
      "https://twitter.com/example",
      "https://github.com/example",
    ],
  };

  return (
    <html lang="ko">
      <body>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        {children}
      </body>
    </html>
  );
}
```

### 블로그 포스트 (Article)

```tsx
// src/app/blog/[slug]/page.tsx
export default async function BlogPostPage({ params }: PageProps) {
  const { slug } = await params;
  const post = await getPost(slug);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      "@type": "Person",
      name: post.author.name,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>{/* ... */}</article>
    </>
  );
}
```

### 상품 (Product)

```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Product",
  name: product.name,
  description: product.description,
  image: product.images,
  offers: {
    "@type": "Offer",
    price: product.price,
    priceCurrency: "KRW",
    availability: product.inStock
      ? "https://schema.org/InStock"
      : "https://schema.org/OutOfStock",
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: product.rating,
    reviewCount: product.reviewCount,
  },
};
```

### FAQ

```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map((faq) => ({
    "@type": "Question",
    name: faq.question,
    acceptedAnswer: {
      "@type": "Answer",
      text: faq.answer,
    },
  })),
};
```

### BreadcrumbList

```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: [
    { "@type": "ListItem", position: 1, name: "홈", item: "https://example.com" },
    { "@type": "ListItem", position: 2, name: "블로그", item: "https://example.com/blog" },
    { "@type": "ListItem", position: 3, name: post.title },
  ],
};
```

## Sitemap

### 정적 Sitemap

```typescript
// src/app/sitemap.ts
import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://example.com",
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: "https://example.com/about",
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.8,
    },
  ];
}
```

### 동적 Sitemap (DB에서 생성)

```typescript
// src/app/sitemap.ts
import type { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await db.post.findMany({
    select: { slug: true, updatedAt: true },
  });

  const postEntries = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: "weekly" as const,
    priority: 0.7,
  }));

  return [
    {
      url: "https://example.com",
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    ...postEntries,
  ];
}
```

### 대규모 사이트맵 (50,000개 초과)

```typescript
// src/app/sitemap/[id]/route.ts — 여러 사이트맵 파일로 분할
export async function generateSitemaps() {
  const totalProducts = await db.product.count();
  const numberOfSitemaps = Math.ceil(totalProducts / 50000);

  return Array.from({ length: numberOfSitemaps }, (_, i) => ({ id: i }));
}

export default async function sitemap({ id }: { id: number }): Promise<MetadataRoute.Sitemap> {
  const start = id * 50000;
  const products = await db.product.findMany({
    skip: start,
    take: 50000,
    select: { slug: true, updatedAt: true },
  });

  return products.map((product) => ({
    url: `https://example.com/products/${product.slug}`,
    lastModified: product.updatedAt,
  }));
}
```

## Robots.txt

```typescript
// src/app/robots.ts
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/admin/", "/private/"],
      },
    ],
    sitemap: "https://example.com/sitemap.xml",
  };
}
```

## 동적 OG 이미지 생성

```tsx
// src/app/api/og/route.tsx
import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";

export const runtime = "edge";

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const title = searchParams.get("title") ?? "Default Title";

  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#0a0a0a",
          color: "#fafafa",
          fontSize: 48,
          fontWeight: 700,
        }}
      >
        <div style={{ marginBottom: 24 }}>사이트명</div>
        <div style={{ fontSize: 32, color: "#a1a1aa" }}>{title}</div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

```tsx
// 페이지에서 동적 OG 이미지 연결
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  return {
    openGraph: {
      images: [`/api/og?title=${encodeURIComponent(post.title)}`],
    },
  };
}
```

## SEO 체크리스트

| 항목 | 설명 | 필수 |
|------|------|------|
| `<title>` | 페이지별 고유 타이틀 (60자 이내) | O |
| `<meta description>` | 페이지별 고유 설명 (155자 이내) | O |
| `<meta viewport>` | `width=device-width, initial-scale=1` | O |
| `<html lang>` | 페이지 언어 설정 (`ko`) | O |
| `<link rel="canonical">` | 정규 URL 설정 (중복 방지) | O |
| Open Graph | `og:title`, `og:description`, `og:image` | O |
| Twitter Card | `twitter:card`, `twitter:title` | 권장 |
| JSON-LD | 구조화 데이터 (페이지 유형별) | 권장 |
| sitemap.xml | 전체 페이지 목록 | O |
| robots.txt | 크롤링 규칙 | O |
| 시맨틱 HTML | `h1`~`h6` 계층, `<main>`, `<article>` 등 | O |
| 이미지 `alt` | 모든 의미 있는 이미지에 대체 텍스트 | O |
| HTTPS | SSL 인증서 적용 | O |
| 모바일 친화적 | 반응형 디자인 | O |
| 페이지 속도 | Core Web Vitals 충족 | 권장 |

## 리포트 형식

```markdown
# SEO Audit: [대상]

## 요약
- SEO 점수: [N/100]
- 필수 항목 누락: N개
- 권장 항목 누락: N개

## 필수 수정
### [S1] 이슈 제목
- **항목**: [title / description / OG / ...]
- **현재**: 없음 또는 현재 값
- **수정안**: 코드

## 권장 개선
...

## 통과 항목
- ...
```

## 실행 규칙

1. 인자가 없으면 프로젝트 전체의 SEO 상태를 점검한다
2. `sitemap` 인자 시 sitemap.ts 파일을 생성/개선한다
3. `og-image` 인자 시 동적 OG 이미지 Route Handler를 생성한다
4. 파일 경로가 전달되면 해당 페이지의 메타데이터를 분석한다
5. `layout.tsx`의 전역 메타데이터와 개별 페이지 메타데이터의 상속 구조를 확인한다
6. `metadataBase`가 설정되어 있는지 확인하고, 없으면 추가를 안내한다
