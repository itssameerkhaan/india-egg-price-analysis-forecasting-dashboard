# OrbitView - Satellite Image Intelligence Portal

## PROJECT OVERVIEW

**OrbitView** is a comprehensive satellite image intelligence portal designed to manage, process, and serve satellite imagery data with automatic GeoServer publishing and PostGIS spatial querying.

### Core Features
- Automatic image upload and processing pipeline
- Cloud Optimized GeoTIFF (COG) conversion with GDAL
- MinIO S3-compatible object storage
- GeoServer WMS/WMTS publishing
- PostGIS spatial database with footprint indexing
- RESTful API with comprehensive image search
- Request correlation IDs for distributed tracing
- Structured logging with file rolling

## TECH STACK

| Category | Technology | Version |
|----------|-----------|---------|
| **Language** | Java | 17 |
| **Framework** | Spring Boot | 4.0.6 |
| **Database** | PostgreSQL + PostGIS | Latest |
| **Storage** | MinIO | S3 API Compatible |
| **Map Server** | GeoServer | 2.x |
| **Geospatial** | GDAL/OGR, JTS, Hibernate Spatial | Latest |
| **Build** | Maven | 3.x |

## PROJECT STRUCTURE

### Source Code Organization

```
src/main/java/com/Orbit_API/
├── OrbitApiApplication.java
│
├── catalog/
│   ├── controller/
│   │   └── SatelliteImageController.java
│   ├── dto/
│   │   ├── ImageResponse.java
│   │   ├── ImageSearchRequest.java
│   │   ├── ImageSearchRequestDTO.java
│   │   ├── ImageStatusResponse.java
│   │   ├── SearchResultDTO.java
│   │   ├── UploadImageRequest.java
│   │   ├── UploadImageRequestDTO.java
│   │   └── UploadImageResponseDTO.java
│   ├── entity/
│   │   ├── AuditLog.java
│   │   ├── ImageProcessingStatus.java
│   │   └── SatelliteImage.java
│   ├── repository/
│   │   ├── AuditLogRepository.java
│   │   └── SatelliteImageRepository.java
│   └── service/
│       ├── AsyncImageProcessingService.java
│       ├── ImageMetadataService.java
│       ├── ImageStatusService.java
│       ├── ImageValidationService.java
│       ├── MinioRetryService.java
│       ├── SatelliteImageService.java
│       └── SatelliteImageServiceImpl.java
│
├── sentinel/
│   ├── controller/
│   │   └── SentinelUploadController.java
│   ├── dto/
│   │   ├── SentinelUploadRequestDTO.java
│   │   ├── SentinelUploadResponseDTO.java
│   │   └── SentinelValidationResponseDTO.java
│   ├── entity/
│   │   └── SentinelBandManifest.java
│   ├── enums/
│   │   ├── BandGroupType.java
│   │   ├── ExportMode.java
│   │   └── UploadMode.java
│   ├── processing/
│   │   └── SentinelGdalService.java
│   └── service/
│       ├── SentinelBandValidationService.java
│       ├── SentinelRgbIngestionService.java
│       └── impl/
│           ├── SentinelBandValidationServiceImpl.java
│           └── SentinelRgbIngestionServiceImpl.java
│
├── export/
│   ├── controller/
│   │   └── RasterExportController.java
│   ├── dto/
│   │   ├── RasterExportRequestDTO.java
│   │   ├── RasterExportResponseDTO.java
│   │   └── RasterExportStatusDTO.java
│   ├── entity/
│   │   ├── ExportFormat.java
│   │   ├── ExportStatus.java
│   │   ├── ExportType.java
│   │   └── RasterExportJob.java
│   ├── exception/
│   │   └── RasterExportException.java
│   ├── mapper/
│   │   └── RasterExportMapper.java
│   ├── processing/
│   │   └── GdalRasterExportService.java
│   ├── repository/
│   │   └── RasterExportJobRepository.java
│   └── service/
│       ├── RasterExportService.java
│       └── impl/
│           └── RasterExportServiceImpl.java
│
├── messaging/
│   ├── config/
│   │   ├── RabbitMQConfig.java
│   │   └── RabbitMQProperties.java
│   ├── consumer/
│   │   ├── ImageIngestConsumer.java
│   │   └── ImageIngestDlqConsumer.java
│   ├── dto/
│   │   └── ImageIngestMessageDTO.java
│   ├── entity/
│   │   └── ImageProcessingJob.java
│   ├── enums/
│   │   ├── JobStatus.java
│   │   └── ProcessingStage.java
│   ├── exception/
│   │   └── MessageProcessingException.java
│   ├── mapper/
│   │   └── ImageIngestMessageMapper.java
│   ├── publisher/
│   │   └── ImageIngestPublisher.java
│   ├── repository/
│   │   └── ImageProcessingJobRepository.java
│   └── service/
│       └── ImageIngestOrchestrator.java
│
├── commom/
│   └── HealthController.java
│
├── config/
│   ├── AsyncConfig.java
│   ├── GeoServerConfig.java
│   ├── LoggingConfig.java
│   ├── MinioConfig.java
│   ├── WebConfig.java
│   └── security/
│       ├── JwtAuthenticationFilter.java
│       ├── JwtTokenProvider.java
│       ├── KeycloakProperties.java
│       └── SecurityConfig.java
│
├── exception/
│   ├── ApiExceptionHandler.java
│   ├── GlobalExceptionHandler.java
│   ├── ImageProcessingException.java
│   ├── NotFoundException.java
│   └── ValidationException.java
│
├── geoserver/
│   ├── GeoServerRestService.java
│   └── ResilientGeoServerService.java
│
├── processing/
│   ├── GdalProcessingService.java
│   └── ImageMetadataService.java
│
├── storage/
│   ├── MinioRetryService.java
│   └── MinioStorageService.java
│
├── users/
│   ├── User.java
│   └── UserRepository.java
│
└── util/
    └── GeoJsonUtil.java


src/main/resources/
├── application.yml
├── logback-spring.xml
└── logback.xml



```

---

## FILE PATHS FOR MANUAL CODE PASTING

### Core Application Files
---

ORBIT API - ALL JAVA SOURCE FILES
========================================================================================================================


---

========================================================================================================================
FILE PATH: Orbit_API/OrbitApiApplication.java
========================================================================================================================

package com.Orbit_API;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrbitApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(OrbitApiApplication.class, args);
	}

}


========================================================================================================================
FILE PATH: Orbit_API/catalog/controller/SatelliteImageController.java
========================================================================================================================

package com.Orbit_API.catalog.controller;

import com.Orbit_API.catalog.dto.ImageResponse;
import com.Orbit_API.catalog.dto.ImageSearchRequest;
import com.Orbit_API.catalog.dto.UploadImageRequest;
import com.Orbit_API.catalog.dto.ImageStatusResponse;
import com.Orbit_API.catalog.dto.UploadImageResponseDTO;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.service.AsyncImageProcessingService;
import com.Orbit_API.catalog.service.ImageStatusService;
import com.Orbit_API.catalog.service.SatelliteImageService;
import com.Orbit_API.exception.ValidationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.Orbit_API.catalog.dto.ImageSearchRequestDTO;
import com.Orbit_API.catalog.dto.SearchResultDTO;
import com.Orbit_API.exception.NotFoundException;
import com.Orbit_API.messaging.service.ImageIngestOrchestrator;

import java.util.List;
import java.util.UUID;

/**
* Satellite Image REST Controller
*
* Endpoints:
* - POST  /api/v1/images/upload       — Queue satellite image for async processing
* - POST  /api/v1/images/search       — Search images by polygon spatial query
* - GET   /api/v1/images/{id}         — Get image metadata by ID
* - GET   /api/v1/images/{id}/status  — Poll processing status and progress
* - GET   /api/v1/images/{id}/download — Get signed download URL
    */
    @Slf4j
    @RestController
    @RequestMapping("/api/v1/images")
    public class SatelliteImageController {

// ── Dependencies ─────────────────────────────────────────────────────────
private final SatelliteImageService        imageService;
private final ImageIngestOrchestrator  imageIngestOrchestrator;
// private final AsyncImageProcessingService  asyncImageProcessingService;
private final ImageStatusService           imageStatusService;

public SatelliteImageController(
SatelliteImageService imageService,
ImageIngestOrchestrator  imageIngestOrchestrator,
ImageStatusService imageStatusService) {
this.imageService               = imageService;
// this.asyncImageProcessingService = asyncImageProcessingService;
this.imageIngestOrchestrator = imageIngestOrchestrator;
this.imageStatusService          = imageStatusService;
}

// ═════════════════════════════════════════════════════════════════════════
// POST /api/v1/images/upload
// ═════════════════════════════════════════════════════════════════════════


    /**
     * POST /api/v1/images/upload
     * NOW publishes to RabbitMQ instead of directly running the pipeline.
     * API contract is IDENTICAL — same request shape, same 202 response shape.
     */
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<UploadImageResponseDTO> upload(
            @RequestPart("meta")  UploadImageRequest request,
            @RequestPart("file")  MultipartFile file) {

        long startTime = System.currentTimeMillis();
        String filename = file.getOriginalFilename();
        long fileSize   = file.getSize();

        log.info("[UPLOAD-START] filename={} size={}MB title={}",
                filename, fileSize / 1024 / 1024, request.getTitle());

        try {
            UploadImageResponseDTO response =
                    imageIngestOrchestrator.queueImageProcessing(file, request, "system");

            long duration = System.currentTimeMillis() - startTime;
            log.info("[UPLOAD-ACCEPTED] imageCode={} trackingUrl={} in {}ms",
                    response.getImageCode(), response.getTrackingUrl(), duration);
            return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);

        } catch (ValidationException ex) {
            log.warn("[UPLOAD-VALIDATION-FAILED] {} in {}ms",
                    ex.getMessage(), System.currentTimeMillis() - startTime);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();

        } catch (Exception ex) {
            log.error("[UPLOAD-FAILED] {} in {}ms",
                    ex.getMessage(), System.currentTimeMillis() - startTime, ex);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }





//
//    /**
//     * Queue a satellite image for async processing.
//     * Returns 202 Accepted immediately with a tracking URL.
//     * Client should poll GET /api/v1/images/{id}/status to track progress.
//     *
//     * @param request  Metadata DTO (title, satellite, sensor, acquisition date, etc.)
//     * @param file     The satellite image file (GeoTIFF, JP2, etc.)
//     * @return UploadImageResponseDTO with imageCode, status=PENDING, trackingUrl
//     */
//    @PostMapping(value = "upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
//    public ResponseEntity<UploadImageResponseDTO> upload(
//            @RequestPart("meta") UploadImageRequest request,
//            @RequestPart("file") MultipartFile file) {
//
//        long startTime = System.currentTimeMillis();
//        String filename = file.getOriginalFilename();
//        long fileSize   = file.getSize();
//
//        log.info("");
//        log.info("[UPLOAD-START] Image upload initiated");
//        log.info("  File Name   : {}", filename);
//        log.info("  File Size   : {} bytes ({} MB)", fileSize, fileSize / 1024 / 1024);
//        log.info("  Title       : {}", request.getTitle());
//        log.info("  Satellite   : {}", request.getSatelliteName());
//        log.info("  Sensor      : {}", request.getSensorName());
//        log.info("  Acquisition : {}", request.getAcquisitionDate());
//
//        try {
//            UploadImageResponseDTO response =
//                    asyncImageProcessingService.queueImageProcessing(file, request, "system");
//
//            long duration = System.currentTimeMillis() - startTime;
//            log.info("[UPLOAD-ACCEPTED] Image queued successfully");
//            log.info("  Image Code   : {}", response.getImageCode());
//            log.info("  Tracking URL : {}", response.getTrackingUrl());
//            log.info("  Execution Time (ms): {}", duration);
//
//            return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);
//
//        } catch (ValidationException ex) {
//            long duration = System.currentTimeMillis() - startTime;
//            log.warn("[UPLOAD-VALIDATION-FAILED] {}", ex.getMessage());
//            log.warn("  File Name          : {}", filename);
//            log.warn("  Execution Time (ms): {}", duration);
//            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
//
//        } catch (Exception ex) {
//            long duration = System.currentTimeMillis() - startTime;
//            log.error("[UPLOAD-FAILED] Upload queuing failed", ex);
//            log.error("  File Name          : {}", filename);
//            log.error("  Error Message      : {}", ex.getMessage());
//            log.error("  Execution Time (ms): {}", duration);
//            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
//        }
//    }







     // ═════════════════════════════════════════════════════════════════════════
     // GET /api/v1/images/{id}/status
    // ═════════════════════════════════════════════════════════════════════════

    /**
     * GET /api/v1/images/{id}/status
     * Poll the async processing status of an image.
     * Called by the frontend every ~3 seconds after upload.
     *
     * @param id Image UUID
     * @return 200 with ImageStatusResponse, or 404 if image not found
     */
    @GetMapping("/{id}/status")
    public ResponseEntity<ImageStatusResponse> getStatus(@PathVariable UUID id) {
        long startTime = System.currentTimeMillis();
        log.debug("[STATUS-POLL] Checking status for image: {}", id);

        // 1. Fetch full entity — null means image does not exist
        SatelliteImage image = imageStatusService.getImageStatus(id);
        if (image == null) {
            long duration = System.currentTimeMillis() - startTime;
            log.warn("[STATUS-NOT-FOUND] Image {} not found ({}ms)", id, duration);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // 2. Derive progress & step from status
        int    progress    = imageStatusService.getProgress(id);
        String currentStep = imageStatusService.getCurrentStep(id);
        String status      = image.getStatus();

        // 3. Populate GeoServer URLs and download URL — only non-null when PUBLISHED
        boolean isPublished = "PUBLISHED".equals(status);
        String downloadUrl  = isPublished
                ? "/api/v1/images/" + id + "/download"
                : null;

        long duration = System.currentTimeMillis() - startTime;
        log.debug("[STATUS-SUCCESS] id={} status={} progress={} step='{}' ({}ms)",
                id, status, progress, currentStep, duration);

        ImageStatusResponse response = ImageStatusResponse.builder()
                .imageId(id)
                .imageCode(image.getImageCode())
                .status(status)
                .progress(progress)
                .currentStep(currentStep)
                .wmsUrl(image.getGeoserverWmsUrl())       // null until PUBLISHED
                .wmtsUrl(image.getGeoserverWmtsUrl())     // null until PUBLISHED
                .downloadUrl(downloadUrl)
                .build();

        return ResponseEntity.ok(response);
    }




//
//    /**
//     * Poll the async processing status of an image.
//     * Returns 200 with progress details, or 404 if image not found.
//     *
//     * @param id  Image UUID
//     * @return ImageStatusResponse with imageId, status, progress (0-100), currentStep
//     */
//    @GetMapping("{id}/status")
//    public ResponseEntity<ImageStatusResponse> getStatus(@PathVariable UUID id) {
//
//        long startTime = System.currentTimeMillis();
//        log.debug("[STATUS-POLL] Checking status for image {}", id);
//
//        // ImageStatusService returns null when image is not found
//        com.Orbit_API.catalog.entity.SatelliteImage image =
//                imageStatusService.getImageStatus(id);
//
//        if (image == null) {
//            long duration = System.currentTimeMillis() - startTime;
//            log.warn("[STATUS-NOT-FOUND] Image {} not found ({}ms)", id, duration);
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
//        }
//
//        int    progress    = imageStatusService.getProgress(id);
//        String currentStep = imageStatusService.getCurrentStep(id);
//        String status      = image.getStatus();
//
//        long duration = System.currentTimeMillis() - startTime;
//        log.debug("[STATUS-SUCCESS] id={} status={} progress={}% step={} ({}ms)",
//                id, status, progress, currentStep, duration);
//
//        return ResponseEntity.ok(new ImageStatusResponse(id, status, progress, currentStep));
//    }

    // ═════════════════════════════════════════════════════════════════════════
    // POST /api/v1/images/search  — UNCHANGED
    // ═════════════════════════════════════════════════════════════════════════

    /**
     * Search images by spatial polygon (Area of Interest).
     * Uses PostGIS ST_Intersects for spatial query.
     *
     * @param request  GeoJSON polygon + optional filters (sensor, cloud cover, etc.)
     * @return List of matching images
     */
    @PostMapping("search")
    public ResponseEntity<List<ImageResponse>> search(@RequestBody ImageSearchRequest request) {

        long startTime = System.currentTimeMillis();
        log.info("[SEARCH-START] Spatial search initiated");
        log.info("  GeoJSON Polygon : {} characters",
                request.getGeoJsonPolygon() != null ? request.getGeoJsonPolygon().length() : 0);
        log.info("  Sensor Filter   : {}", request.getSensorName());
        log.info("  Cloud Cover Max : {}", request.getMaxCloudCover());

        try {
            List<ImageResponse> results = imageService.searchByPolygon(request);
            long duration = System.currentTimeMillis() - startTime;
            log.info("[SEARCH-SUCCESS] Results found: {} ({}ms)", results.size(), duration);
            return ResponseEntity.ok(results);

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[SEARCH-FAILED] Search operation failed ({}ms)", duration, ex);
            log.error("  Error Message: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GET /api/v1/images/{id}  — UNCHANGED
    // ═════════════════════════════════════════════════════════════════════════

    /**
     * Get full image metadata by UUID.
     *
     * @param id  Image UUID
     * @return ImageResponse with full metadata
     */
    @GetMapping("{id}")
    public ResponseEntity<ImageResponse> getById(@PathVariable UUID id) {

        long startTime = System.currentTimeMillis();
        log.debug("[GET-BY-ID] Fetching image {}", id);

        try {
            ImageResponse response = imageService.getById(id);
            long duration = System.currentTimeMillis() - startTime;
            log.info("[GET-BY-ID-SUCCESS] Image retrieved: {} ({}ms)",
                    response.getImageCode(), duration);
            return ResponseEntity.ok(response);

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.warn("[GET-BY-ID-FAILED] Image not found or error for id={} ({}ms)", id, duration);
            log.debug("  Error Message: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GET /api/v1/images/{id}/download  — UNCHANGED
    // ═════════════════════════════════════════════════════════════════════════

    /**
     * Get a signed MinIO download URL. Valid for 60 minutes.
     *
     * @param id  Image UUID
     * @return Signed download URL string
     */
    @GetMapping("{id}/download")
    public ResponseEntity<String> download(@PathVariable UUID id) {

        long startTime = System.currentTimeMillis();
        log.info("[DOWNLOAD-URL-START] Generating signed download URL for {}", id);

        try {
            String downloadUrl = imageService.getDownloadUrl(id);
            long duration = System.currentTimeMillis() - startTime;
            log.info("[DOWNLOAD-URL-SUCCESS] Signed URL generated ({}ms)", duration);
            log.debug("  Image ID: {}", id);
            return ResponseEntity.ok(downloadUrl);

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[DOWNLOAD-URL-FAILED] Failed to generate download URL ({}ms)", duration, ex);
            log.error("  Image ID      : {}", id);
            log.error("  Error Message : {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    // ═════════════════════════════════════════════════════════════════════════
    // Inner response record — status polling response shape
    // ═════════════════════════════════════════════════════════════════════════

    /**
     * Response body for GET /api/v1/images/{id}/status
     */


    // =========================================================================
// POST /api/v1/images/search/full
// Full paginated spatial search with all filters.
// Uses ImageSearchRequestDTO (validated) instead of legacy ImageSearchRequest.
// Returns SearchResultDTO with results, totalCount, page, pageSize, totalPages.
// =========================================================================

    /**
     * Full paginated search by spatial polygon with all filter options.
     * Supports date range, satellite, cloud cover, resolution, and pagination.
     *
     * @param request Full search DTO with GeoJSON polygon, filters, and pagination
     * @return SearchResultDTO with paginated image results and total count
     */
    @PostMapping("/search/full")
    public ResponseEntity<SearchResultDTO> searchFull(
            @RequestBody @jakarta.validation.Valid ImageSearchRequestDTO request) {

        long startTime = System.currentTimeMillis();

        log.info("[SEARCH-FULL-START] Full paginated spatial search initiated");
        log.info("  GeoJSON length  : {}", request.getGeoJsonPolygon() != null
                ? request.getGeoJsonPolygon().length() : 0);
        log.info("  Satellite       : {}", request.getSatellite());
        log.info("  MaxCloudCover   : {}", request.getMaxCloudCover());
        log.info("  MinResolutionM  : {}", request.getMinResolutionM());
        log.info("  DateFrom        : {}", request.getDateFrom());
        log.info("  DateTo          : {}", request.getDateTo());
        log.info("  Page / PageSize : {} / {}", request.getPage(), request.getPageSize());

        try {
            SearchResultDTO result = imageService.searchByPolygonFull(request);

            long duration = System.currentTimeMillis() - startTime;
            log.info("[SEARCH-FULL-SUCCESS] {} results (total={}) page={} in {}ms",
                    result.getResults().size(), result.getTotalCount(),
                    result.getPage(), duration);

            return ResponseEntity.ok(result);

        } catch (ValidationException ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.warn("[SEARCH-FULL-VALIDATION-FAILED] {} ({}ms)", ex.getMessage(), duration);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[SEARCH-FULL-FAILED] Search failed in {}ms: {}", duration, ex.getMessage(), ex);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    /**
     * DELETE /api/v1/images/{id}
     * Deletes a satellite image and all associated resources:
     * MinIO raw, COG, thumbnail + GeoServer layer + database record.
     *
     * @param id Image UUID
     * @return 204 No Content on success, 404 if image not found
     */
    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Void> deleteImage(@PathVariable UUID id) {
        long startTime = System.currentTimeMillis();
        log.info("[DELETE-REQUEST] Received delete request for image id={}", id);
        try {
            imageService.deleteImage(id);
            long duration = System.currentTimeMillis() - startTime;
            log.info("[DELETE-SUCCESS] Image deleted in {}ms, id={}", duration, id);
            return ResponseEntity.noContent().build();  // 204
        } catch (NotFoundException ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.warn("[DELETE-NOT-FOUND] Image not found in {}ms, id={}", duration, id);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();  // 404
        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[DELETE-FAILED] Unexpected error deleting image id={} in {}ms: {}",
                    id, duration, ex.getMessage(), ex);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();  // 500
        }
    }


}

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/ImageResponse.java
========================================================================================================================

package com.Orbit_API.catalog.dto;



import java.time.LocalDate;
import java.util.UUID;


public class ImageResponse {
private UUID id;
private String imageCode;
private String title;
private String sensorName;
private String satelliteName;
private String processingLevel;
private LocalDate acquisitionDate;
private Double cloudCover;
private Double resolutionM;
private String geoserverLayerName;
private String geoserverWmsUrl;
private String geoserverWmtsUrl;
private String thumbnailPath;
private String footprintGeoJson;

	public UUID getId() {
		return id;
	}
	public void setId(UUID id) {
		this.id = id;
	}
	public String getImageCode() {
		return imageCode;
	}
	public void setImageCode(String imageCode) {
		this.imageCode = imageCode;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getSensorName() {
		return sensorName;
	}
	public void setSensorName(String sensorName) {
		this.sensorName = sensorName;
	}
	public String getSatelliteName() {
		return satelliteName;
	}
	public void setSatelliteName(String satelliteName) {
		this.satelliteName = satelliteName;
	}
	public String getProcessingLevel() {
		return processingLevel;
	}
	public void setProcessingLevel(String processingLevel) {
		this.processingLevel = processingLevel;
	}
	public LocalDate getAcquisitionDate() {
		return acquisitionDate;
	}
	public void setAcquisitionDate(LocalDate acquisitionDate) {
		this.acquisitionDate = acquisitionDate;
	}
	public Double getCloudCover() {
		return cloudCover;
	}
	public void setCloudCover(Double cloudCover) {
		this.cloudCover = cloudCover;
	}
	public Double getResolutionM() {
		return resolutionM;
	}
	public void setResolutionM(Double resolutionM) {
		this.resolutionM = resolutionM;
	}
	public String getGeoserverLayerName() {
		return geoserverLayerName;
	}
	public void setGeoserverLayerName(String geoserverLayerName) {
		this.geoserverLayerName = geoserverLayerName;
	}
	public String getGeoserverWmsUrl() {
		return geoserverWmsUrl;
	}
	public void setGeoserverWmsUrl(String geoserverWmsUrl) {
		this.geoserverWmsUrl = geoserverWmsUrl;
	}
	public String getGeoserverWmtsUrl() {
		return geoserverWmtsUrl;
	}
	public void setGeoserverWmtsUrl(String geoserverWmtsUrl) {
		this.geoserverWmtsUrl = geoserverWmtsUrl;
	}
	public String getThumbnailPath() {
		return thumbnailPath;
	}
	public void setThumbnailPath(String thumbnailPath) {
		this.thumbnailPath = thumbnailPath;
	}
    public String getFootprintGeoJson() { return footprintGeoJson; }
    public void setFootprintGeoJson(String footprintGeoJson) { this.footprintGeoJson = footprintGeoJson; }






}

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/ImageSearchRequest.java
========================================================================================================================

package com.Orbit_API.catalog.dto;


public class ImageSearchRequest {
private String geoJsonPolygon; // polygon sent from OpenLayers
private String sensorName;
private Double maxCloudCover;


	public String getGeoJsonPolygon() {
		return geoJsonPolygon;
	}
	public void setGeoJsonPolygon(String geoJsonPolygon) {
		this.geoJsonPolygon = geoJsonPolygon;
	}
	public String getSensorName() {
		return sensorName;
	}
	public void setSensorName(String sensorName) {
		this.sensorName = sensorName;
	}
	public Double getMaxCloudCover() {
		return maxCloudCover;
	}
	public void setMaxCloudCover(Double maxCloudCover) {
		this.maxCloudCover = maxCloudCover;
	}





}

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/ImageSearchRequestDTO.java
========================================================================================================================

package com.Orbit_API.catalog.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

/**
* PRODUCTION DTO - Image search request with pagination & validation
  */
  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  @Schema(description = "Spatial image search request")
  public class ImageSearchRequestDTO {

  @NotBlank(message = "GeoJSON polygon required")
  @Schema(description = "GeoJSON polygon for Area of Interest", example = "{\"type\":\"Polygon\",\"coordinates\":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}")
  private String geoJsonPolygon;

  @Schema(description = "Start date filter")
  private LocalDate dateFrom;

  @Schema(description = "End date filter")
  private LocalDate dateTo;

  @Pattern(regexp = "^(Landsat-8|Landsat-9|Sentinel-2|Sentinel-1|Planet|MODIS|Gaofen|WorldView|ANY)$",
  message = "Invalid satellite")
  @Schema(description = "Satellite filter", example = "Sentinel-2")
  private String satellite;

  @Min(value = 0, message = "Min cloud cover must be >= 0")
  @Max(value = 100, message = "Max cloud cover must be <= 100")
  @Schema(description = "Maximum cloud cover percentage", example = "30")
  private Double maxCloudCover;

  @Min(value = 1, message = "Min resolution must be > 0")
  @Schema(description = "Minimum resolution in meters", example = "10")
  private Double minResolutionM;

  @Pattern(regexp = "^(Multispectral|Panchromatic|SAR|Hyperspectral|Thermal|ANY)$",
  message = "Invalid band type")
  @Schema(description = "Band type filter", example = "Multispectral")
  private String bandType;

  @Pattern(regexp = "^(L1C|L2A|L2B|L3|L4|ANY)$", message = "Invalid processing level")
  @Schema(description = "Processing level filter", example = "L2A")
  private String processingLevel;

  // PAGINATION
  @Min(value = 0, message = "Page must be >= 0")
  @Schema(description = "Page number (0-indexed)", example = "0")
  @Builder.Default
  private Integer page = 0;

  @Min(value = 1, message = "Page size must be >= 1")
  @Max(value = 1000, message = "Page size must be <= 1000")
  @Schema(description = "Results per page", example = "20")
  @Builder.Default
  private Integer pageSize = 20;

  @Pattern(regexp = "^(acquisitionDate|cloudCover|resolutionM|createdAt)$",
  message = "Invalid sort field")
  @Schema(description = "Sort field", example = "acquisitionDate")
  private String sortBy;

  @Pattern(regexp = "^(ASC|DESC)$", message = "Sort direction must be ASC or DESC")
  @Schema(description = "Sort direction", example = "DESC")
  @Builder.Default
  private String sortDirection = "DESC";
  }

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/ImageStatusResponse.java
========================================================================================================================

package com.Orbit_API.catalog.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

/**
* Response DTO for GET /api/v1/images/{id}/status
* Polled by the frontend every 3 seconds after upload.
  */
  @Data
  @Builder
  @NoArgsConstructor
  @AllArgsConstructor
  @Schema(description = "Image processing status response for polling")
  public class ImageStatusResponse {

  @Schema(description = "Image UUID", example = "3fa85f64-5717-4562-b3fc-2c963f66afa6")
  private UUID imageId;

  @Schema(description = "Unique image code", example = "IMG-3fa85f64-5717-4562-b3fc-2c963f66afa6")
  private String imageCode;

  @Schema(description = "Current processing status", example = "PROCESSING")
  private String status;

  @Schema(description = "Progress percentage (0–100), or -1 if failed", example = "50")
  private int progress;

  @Schema(description = "Human-readable description of the current step",
  example = "Converting to COG")
  private String currentStep;

  @Schema(description = "WMS URL — null until image is PUBLISHED",
  example = "http://localhost:8090/geoserver/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=satellite-portal:IMG-xxx")
  private String wmsUrl;

  @Schema(description = "WMTS URL — null until image is PUBLISHED",
  example = "http://localhost:8090/geoserver/gwc/service/wmts?SERVICE=WMTS&REQUEST=GetCapabilities")
  private String wmtsUrl;

  @Schema(description = "Download URL — null until image is PUBLISHED",
  example = "/api/v1/images/3fa85f64-5717-4562-b3fc-2c963f66afa6/download")
  private String downloadUrl;
  }


========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/SearchResultDTO.java
========================================================================================================================

package com.Orbit_API.catalog.dto;

import java.util.List;

/**
* Paginated search result wrapper for spatial image queries.
* totalPages is pre-calculated so the frontend never divides by zero.
  */
  public class SearchResultDTO {

  private List<ImageResponse> results;
  private long totalCount;
  private int page;
  private int pageSize;
  private int totalPages;

  public SearchResultDTO() {}

  public SearchResultDTO(List<ImageResponse> results, long totalCount, int page, int pageSize) {
  this.results   = results;
  this.totalCount = totalCount;
  this.page      = page;
  this.pageSize  = pageSize;
  this.totalPages = (pageSize > 0)
  ? (int) Math.ceil((double) totalCount / pageSize)
  : 0;
  }

  // ── Getters & Setters ─────────────────────────────────────────────────────

  public List<ImageResponse> getResults()  { return results; }
  public void setResults(List<ImageResponse> results) { this.results = results; }

  public long getTotalCount()              { return totalCount; }
  public void setTotalCount(long totalCount) { this.totalCount = totalCount; }

  public int getPage()                     { return page; }
  public void setPage(int page)            { this.page = page; }

  public int getPageSize()                 { return pageSize; }
  public void setPageSize(int pageSize)    { this.pageSize = pageSize; }

  public int getTotalPages()               { return totalPages; }
  public void setTotalPages(int totalPages){ this.totalPages = totalPages; }
  }

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/UploadImageRequest.java
========================================================================================================================

package com.Orbit_API.catalog.dto;



import java.time.LocalDate;


public class UploadImageRequest {
private String title;
private String sensorName;
private String satelliteName;
private String processingLevel;
private LocalDate acquisitionDate;
private Double cloudCover;
private Double resolutionM;
public String getTitle() {
return title;
}
public void setTitle(String title) {
this.title = title;
}
public String getSensorName() {
return sensorName;
}
public void setSensorName(String sensorName) {
this.sensorName = sensorName;
}
public String getSatelliteName() {
return satelliteName;
}
public void setSatelliteName(String satelliteName) {
this.satelliteName = satelliteName;
}
public String getProcessingLevel() {
return processingLevel;
}
public void setProcessingLevel(String processingLevel) {
this.processingLevel = processingLevel;
}
public LocalDate getAcquisitionDate() {
return acquisitionDate;
}
public void setAcquisitionDate(LocalDate acquisitionDate) {
this.acquisitionDate = acquisitionDate;
}
public Double getCloudCover() {
return cloudCover;
}
public void setCloudCover(Double cloudCover) {
this.cloudCover = cloudCover;
}
public Double getResolutionM() {
return resolutionM;
}
public void setResolutionM(Double resolutionM) {
this.resolutionM = resolutionM;
}





}

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/UploadImageRequestDTO.java
========================================================================================================================

package com.Orbit_API.catalog.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

/**
* PRODUCTION DTO - Request validation for image upload
* Validates: file type, metadata completeness, constraints
  */
  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  @Schema(description = "Satellite image upload request with comprehensive validation")
  public class UploadImageRequestDTO {

  @NotBlank(message = "Title is required")
  @Size(min = 3, max = 255, message = "Title must be between 3-255 characters")
  @Schema(description = "Human-readable image title", example = "Landsat-8 Urban Area")
  private String title;

  @NotBlank(message = "Satellite name is required")
  @Pattern(regexp = "^(Landsat-8|Landsat-9|Sentinel-2|Sentinel-1|Planet|MODIS|Gaofen|WorldView)$",
  message = "Satellite must be from approved list")
  @Schema(description = "Satellite name", example = "Sentinel-2")
  private String satelliteName;

  @NotBlank(message = "Sensor name is required")
  @Size(min = 2, max = 100, message = "Sensor name must be 2-100 chars")
  @Schema(description = "Sensor name/identifier", example = "MSI")
  private String sensorName;

  @NotNull(message = "Acquisition date is required")
  @Schema(description = "Date image was acquired", example = "2026-05-01")
  private LocalDate acquisitionDate;

  @NotNull(message = "Cloud cover is required")
  @Min(value = 0, message = "Cloud cover must be >= 0%")
  @Max(value = 100, message = "Cloud cover must be <= 100%")
  @Schema(description = "Cloud cover percentage", example = "15.5")
  private Double cloudCover;

  @NotNull(message = "Resolution is required")
  @Min(value = 1, message = "Resolution must be at least 1 meter")
  @Max(value = 1000, message = "Resolution must be <= 1000 meters")
  @Schema(description = "Ground sample distance in meters", example = "30.0")
  private Double resolutionM;

  @NotNull(message = "Processing level is required")
  @Pattern(regexp = "^(L1C|L2A|L2B|L3|L4)$", message = "Processing level must be L1C, L2A, L2B, L3, or L4")
  @Schema(description = "Processing level", example = "L2A")
  private String processingLevel;

  @NotNull(message = "Band type is required")
  @Pattern(regexp = "^(Multispectral|Panchromatic|SAR|Hyperspectral|Thermal)$",
  message = "Band type must be valid")
  @Schema(description = "Band type", example = "Multispectral")
  private String bandType;

  @Size(min = 0, max = 10, message = "Maximum 10 bands")
  @Schema(description = "Band details list")
  private List<BandDetailDTO> bands;

  @NotNull(message = "File format is required")
  @Pattern(regexp = "^(GeoTIFF|JPEG2000|NITF|ENVI)$", message = "Format must be GeoTIFF, JPEG2000, NITF, or ENVI")
  @Schema(description = "File format", example = "GeoTIFF")
  private String fileFormat;

  @Size(max = 500, message = "Description max 500 chars")
  @Schema(description = "Optional image description")
  private String description;

  // Derived from file upload - NOT from user
  @Schema(hidden = true)
  private String originalFileName;

  @Schema(hidden = true)
  private Long fileSizeBytes;

  @Schema(hidden = true)
  private String fileChecksum; // MD5/SHA256 from client

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  @Builder
  public static class BandDetailDTO {
  @NotBlank(message = "Band name is required")
  private String bandName;

       @NotNull(message = "Band number is required")
       @Min(1)
       @Max(999)
       private Integer bandNumber;

       private String wavelengthRange;
  }
  }

========================================================================================================================
FILE PATH: Orbit_API/catalog/dto/UploadImageResponseDTO.java
========================================================================================================================

package com.Orbit_API.catalog.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Upload response with tracking URL")
public class UploadImageResponseDTO {

    @Schema(description = "Unique image code", example = "IMG-a1b2c3d4-e5f6-7890-abcd-ef1234567890")
    private String imageCode;

    @Schema(description = "Processing status", example = "PENDING")
    private String status;

    @Schema(description = "URL to check status", example = "/api/v1/images/[ID]/status")
    private String trackingUrl;

    @Schema(description = "Informational message", example = "Image queued for processing")
    private String message;

    @Schema(description = "WMS URL (after processing)", example = "http://localhost:8090/geoserver/wms?...")
    private String wmsUrl;

    @Schema(description = "WMTS URL (after processing)", example = "http://localhost:8090/geoserver/wmts?...")
    private String wmtsUrl;

    @Schema(description = "Download URL (after processing)", example = "/api/v1/images/[ID]/download")
    private String downloadUrl;

    @Schema(description = "Thumbnail URL (after processing)", example = "/api/v1/images/[ID]/thumbnail")
    private String thumbnailUrl;
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/entity/AuditLog.java
========================================================================================================================

package com.Orbit_API.catalog.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "audit_logs", indexes = {
@Index(name = "idx_audit_logs_user_id", columnList = "user_id"),
@Index(name = "idx_audit_logs_resource_id", columnList = "resource_id"),
@Index(name = "idx_audit_logs_created_at", columnList = "created_at")
})
public class AuditLog {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "user_id", nullable = false)
    private String userId;

    @Column(name = "action", nullable = false)
    private String action;  // e.g., IMAGE_UPLOADED, IMAGE_DELETED, SEARCH_PERFORMED

    @Column(name = "resource_id")
    private String resourceId;  // e.g., image ID

    @Column(name = "resource_type")
    private String resourceType;  // e.g., IMAGE, LAYER, USER

    @Column(name = "status", nullable = false)
    private String status;  // SUCCESS, FAILURE, etc.

    @Column(name = "details", columnDefinition = "TEXT")
    private String details;  // JSON details

    @Column(name = "ip_address")
    private String ipAddress;

    @Column(name = "correlation_id")
    private String correlationId;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/entity/ImageProcessingStatus.java
========================================================================================================================

package com.Orbit_API.catalog.entity;

public enum ImageProcessingStatus {
PENDING,                 // Initial state, waiting for processing
PROCESSING,              // Currently processing
PROCESSING_COMPLETE,     // Processing done, ready for GeoServer
PUBLISHED,               // Successfully published to GeoServer
PUBLISHED_FAILED,        // Published to GeoServer, but layer creation failed
FAILED                   // Processing failed, manual intervention needed
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/entity/SatelliteImage.java
========================================================================================================================

package com.Orbit_API.catalog.entity;

import jakarta.persistence.*;
import org.locationtech.jts.geom.Polygon;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "satellite_images")
public class SatelliteImage {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "image_code", unique = true, nullable = false)
    private String imageCode;

    @Column(name = "title")
    private String title;

    @Column(name = "sensor_name")
    private String sensorName;

    @Column(name = "satellite_name")
    private String satelliteName;

    @Column(name = "processing_level")
    private String processingLevel;

    @Column(name = "acquisition_date")
    private LocalDate acquisitionDate;

    @Column(name = "cloud_cover")
    private Double cloudCover;

    @Column(name = "resolution_m")
    private Double resolutionM;

    @Column(name = "crs_epsg")
    private Integer crsEpsg;

    @Column(columnDefinition = "geometry(Polygon,4326)")
    private Polygon footprint;

    @Column(name = "raw_object_path")
    private String rawObjectPath;

    @Column(name = "cog_object_path")
    private String cogObjectPath;

    @Column(name = "thumbnail_path")
    private String thumbnailPath;

    @Column(name = "geoserver_layer_name")
    private String geoserverLayerName;

    @Column(name = "geoserver_wms_url")
    private String geoserverWmsUrl;

    @Column(name = "geoserver_wmts_url")
    private String geoserverWmtsUrl;

    @Column(name = "status")
    private String status;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "upload_mode")
    private String uploadMode;              // SINGLE_FILE_MODE / SENTINEL_RGB_MODE / etc.

    @Column(name = "preview_png_path")
    private String previewPngPath;          // MinIO path to generated PNG preview

    @Column(name = "preview_jpeg_path")
    private String previewJpegPath;         // MinIO path to generated JPEG preview

    @Column(name = "band_manifest_json", columnDefinition = "TEXT")
    private String bandManifestJson;        // JSON of SentinelBandManifest

    @Column(name = "source_product_name")
    private String sourceProductName;       // S2A_MSIL2A_...

    @Column(name = "tile_id")
    private String tileId;                  // T43RGP
    


    public SatelliteImage() {
		super();
	}

	public SatelliteImage(UUID id, String imageCode, String title, String sensorName, String satelliteName,
			String processingLevel, LocalDate acquisitionDate, Double cloudCover, Double resolutionM, Integer crsEpsg,
			Polygon footprint, String rawObjectPath, String cogObjectPath, String thumbnailPath,
			String geoserverLayerName, String geoserverWmsUrl, String geoserverWmtsUrl, String status,
			LocalDateTime createdAt, LocalDateTime updatedAt) {
		super();
		this.id = id;
		this.imageCode = imageCode;
		this.title = title;
		this.sensorName = sensorName;
		this.satelliteName = satelliteName;
		this.processingLevel = processingLevel;
		this.acquisitionDate = acquisitionDate;
		this.cloudCover = cloudCover;
		this.resolutionM = resolutionM;
		this.crsEpsg = crsEpsg;
		this.footprint = footprint;
		this.rawObjectPath = rawObjectPath;
		this.cogObjectPath = cogObjectPath;
		this.thumbnailPath = thumbnailPath;
		this.geoserverLayerName = geoserverLayerName;
		this.geoserverWmsUrl = geoserverWmsUrl;
		this.geoserverWmtsUrl = geoserverWmtsUrl;
		this.status = status;
		this.createdAt = createdAt;
		this.updatedAt = updatedAt;
	}

	public UUID getId() {
		return id;
	}

	public void setId(UUID id) {
		this.id = id;
	}

	public String getImageCode() {
		return imageCode;
	}

	public void setImageCode(String imageCode) {
		this.imageCode = imageCode;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getSensorName() {
		return sensorName;
	}

	public void setSensorName(String sensorName) {
		this.sensorName = sensorName;
	}

	public String getSatelliteName() {
		return satelliteName;
	}

	public void setSatelliteName(String satelliteName) {
		this.satelliteName = satelliteName;
	}

	public String getProcessingLevel() {
		return processingLevel;
	}

	public void setProcessingLevel(String processingLevel) {
		this.processingLevel = processingLevel;
	}

	public LocalDate getAcquisitionDate() {
		return acquisitionDate;
	}

	public void setAcquisitionDate(LocalDate acquisitionDate) {
		this.acquisitionDate = acquisitionDate;
	}

	public Double getCloudCover() {
		return cloudCover;
	}

	public void setCloudCover(Double cloudCover) {
		this.cloudCover = cloudCover;
	}

	public Double getResolutionM() {
		return resolutionM;
	}

	public void setResolutionM(Double resolutionM) {
		this.resolutionM = resolutionM;
	}

	public Integer getCrsEpsg() {
		return crsEpsg;
	}

	public void setCrsEpsg(Integer crsEpsg) {
		this.crsEpsg = crsEpsg;
	}

	public Polygon getFootprint() {
		return footprint;
	}

	public void setFootprint(Polygon footprint) {
		this.footprint = footprint;
	}

	public String getRawObjectPath() {
		return rawObjectPath;
	}

	public void setRawObjectPath(String rawObjectPath) {
		this.rawObjectPath = rawObjectPath;
	}

	public String getCogObjectPath() {
		return cogObjectPath;
	}

	public void setCogObjectPath(String cogObjectPath) {
		this.cogObjectPath = cogObjectPath;
	}

	public String getThumbnailPath() {
		return thumbnailPath;
	}

	public void setThumbnailPath(String thumbnailPath) {
		this.thumbnailPath = thumbnailPath;
	}

	public String getGeoserverLayerName() {
		return geoserverLayerName;
	}

	public void setGeoserverLayerName(String geoserverLayerName) {
		this.geoserverLayerName = geoserverLayerName;
	}

	public String getGeoserverWmsUrl() {
		return geoserverWmsUrl;
	}

	public void setGeoserverWmsUrl(String geoserverWmsUrl) {
		this.geoserverWmsUrl = geoserverWmsUrl;
	}

	public String getGeoserverWmtsUrl() {
		return geoserverWmtsUrl;
	}

	public void setGeoserverWmtsUrl(String geoserverWmtsUrl) {
		this.geoserverWmtsUrl = geoserverWmtsUrl;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}

	public LocalDateTime getUpdatedAt() {
		return updatedAt;
	}

	public void setUpdatedAt(LocalDateTime updatedAt) {
		this.updatedAt = updatedAt;
	}
    // ── Add getters/setters ───────────────────────────────────────────────────
    public String getUploadMode()                       { return uploadMode; }
    public void setUploadMode(String m)                 { this.uploadMode = m; }
    public String getPreviewPngPath()                   { return previewPngPath; }
    public void setPreviewPngPath(String p)             { this.previewPngPath = p; }
    public String getPreviewJpegPath()                  { return previewJpegPath; }
    public void setPreviewJpegPath(String p)            { this.previewJpegPath = p; }
    public String getBandManifestJson()                 { return bandManifestJson; }
    public void setBandManifestJson(String j)           { this.bandManifestJson = j; }
    public String getSourceProductName()                { return sourceProductName; }
    public void setSourceProductName(String s)          { this.sourceProductName = s; }
    public String getTileId()                           { return tileId; }
    public void setTileId(String t)                     { this.tileId = t; }

	@PrePersist
    public void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
        if (this.status == null) this.status = "UPLOADED";
    }

    @PreUpdate
    public void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/repository/AuditLogRepository.java
========================================================================================================================

package com.Orbit_API.catalog.repository;

import com.Orbit_API.catalog.entity.AuditLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, UUID> {
List<AuditLog> findByUserIdOrderByCreatedAtDesc(String userId);
List<AuditLog> findByResourceIdOrderByCreatedAtDesc(String resourceId);
List<AuditLog> findByActionAndCreatedAtAfter(String action, LocalDateTime createdAt);
List<AuditLog> findByCorrelationId(String correlationId);
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/repository/SatelliteImageRepository.java
========================================================================================================================

package com.Orbit_API.catalog.repository;

import com.Orbit_API.catalog.entity.SatelliteImage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Repository
public interface SatelliteImageRepository extends JpaRepository<SatelliteImage, UUID> {

    @Query(value = """
            SELECT *
            FROM satellite_images s
            WHERE ST_Intersects(
                      s.footprint,
                      ST_SetSRID(ST_GeomFromGeoJSON(:geoJsonPolygon), 4326)
                  )
              AND s.status = 'PUBLISHED'
              AND (:sensorName     IS NULL OR LOWER(s.sensor_name)     = LOWER(:sensorName))
              AND (:satellite      IS NULL OR LOWER(s.satellite_name)  = LOWER(:satellite))
              AND (:maxCloudCover  IS NULL OR s.cloud_cover           <= :maxCloudCover)
              AND (:minResolutionM IS NULL OR s.resolution_m          >= :minResolutionM)
              AND (CAST(:dateFrom AS date) IS NULL OR s.acquisition_date >= CAST(:dateFrom AS date))
              AND (CAST(:dateTo   AS date) IS NULL OR s.acquisition_date <= CAST(:dateTo   AS date))
            ORDER BY s.acquisition_date DESC
            LIMIT  :limit
            OFFSET :offset
            """,
            nativeQuery = true)
    List<SatelliteImage> searchByPolygon(
            @Param("geoJsonPolygon") String geoJsonPolygon,
            @Param("sensorName")     String sensorName,
            @Param("satellite")      String satellite,
            @Param("maxCloudCover")  Double maxCloudCover,
            @Param("minResolutionM") Double minResolutionM,
            @Param("dateFrom")       LocalDate dateFrom,
            @Param("dateTo")         LocalDate dateTo,
            @Param("limit")          int limit,
            @Param("offset")         int offset
    );

    @Query(value = """
            SELECT COUNT(*)
            FROM satellite_images s
            WHERE ST_Intersects(
                      s.footprint,
                      ST_SetSRID(ST_GeomFromGeoJSON(:geoJsonPolygon), 4326)
                  )
              AND s.status = 'PUBLISHED'
              AND (:sensorName     IS NULL OR LOWER(s.sensor_name)     = LOWER(:sensorName))
              AND (:satellite      IS NULL OR LOWER(s.satellite_name)  = LOWER(:satellite))
              AND (:maxCloudCover  IS NULL OR s.cloud_cover           <= :maxCloudCover)
              AND (:minResolutionM IS NULL OR s.resolution_m          >= :minResolutionM)
              AND (CAST(:dateFrom AS date) IS NULL OR s.acquisition_date >= CAST(:dateFrom AS date))
              AND (CAST(:dateTo   AS date) IS NULL OR s.acquisition_date <= CAST(:dateTo   AS date))
            """,
            nativeQuery = true)
    long countByPolygon(
            @Param("geoJsonPolygon") String geoJsonPolygon,
            @Param("sensorName")     String sensorName,
            @Param("satellite")      String satellite,
            @Param("maxCloudCover")  Double maxCloudCover,
            @Param("minResolutionM") Double minResolutionM,
            @Param("dateFrom")       LocalDate dateFrom,
            @Param("dateTo")         LocalDate dateTo
    );
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/service/AsyncImageProcessingService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

import com.Orbit_API.catalog.dto.UploadImageResponseDTO;
import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.exception.ImageProcessingException;
import com.Orbit_API.exception.ValidationException;
import com.Orbit_API.geoserver.GeoServerRestService;
import com.Orbit_API.processing.GdalProcessingService;
import com.Orbit_API.storage.MinioStorageService;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Polygon;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import com.Orbit_API.catalog.dto.UploadImageRequest;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.UUID;

/**
* Asynchronous Image Processing Service
*
* Flow:
*  1. validateUploadRequest()
*  2. createPendingImageRecord()  (status = PENDING)
*  3. processImageAsync() runs in background thread:
*     - GDAL metadata + COG
*     - upload raw + COG to MinIO
*     - copy COG to GeoServer shared dir
*     - publish layer to GeoServer
*  4. On failure: mark FAILED and try to rollback MinIO objects
      */
      @Slf4j
      @Service
      public class AsyncImageProcessingService {

private final SatelliteImageRepository imageRepository;
private final GdalProcessingService gdalService;
private final MinioStorageService minioService;
private final GeoServerRestService geoServerService;
private final ImageValidationService validationService;

@Value("${app.upload.max-file-size:2147483648}")  // 2GB default
private long maxFileSize;

@Value("${app.upload.temp-dir:/tmp/orbitview}")
private String tempDirectory;

@Value("${geoserver.publish.retry-attempts:3}")
private int geoServerRetryAttempts;

@Value("${minio.upload.retry-attempts:3}")
private int minioRetryAttempts;

@Value("${minio.bucket-raw}")
private String rawBucket;

@Value("${minio.bucket-cog}")
private String cogBucket;

@Value("${orbitview.shared-data-dir}")
private String sharedDataDir;

public AsyncImageProcessingService(
SatelliteImageRepository imageRepository,
GdalProcessingService gdalService,
MinioStorageService minioService,
GeoServerRestService geoServerService,
ImageValidationService validationService
) {
this.imageRepository = imageRepository;
this.gdalService = gdalService;
this.minioService = minioService;
this.geoServerService = geoServerService;
this.validationService = validationService;
}

/**
    * Entry point from controller/service layer.
    * Validates and registers the image, then triggers async processing and returns immediately.
      */
      //    @Transactional
      //    public UploadImageResponseDTO queueImageProcessing(
      //            MultipartFile file,
      //            String metadata,   // reserved for future use
      //            String userId      // reserved for future use
      //    ) throws ValidationException {
      //
      //        log.info("UPLOAD_START: user={}, filename={}, size={}",
      //                userId, file.getOriginalFilename(), file.getSize());
      //
      //        // 1. VALIDATE
      //        validateUploadRequest(file);
      //
      //        // 2. PRE-REGISTER (PENDING)
      //        SatelliteImage image = createPendingImageRecord(file);
      //        log.info("UPLOAD_REGISTERED: imageCode={}, status=PENDING", image.getImageCode());
      //
      //        // 3. ASYNC BACKGROUND PROCESS
      //        processImageAsync(image, file);
      //
      //        // 4. IMMEDIATE RESPONSE (client polls status endpoint)
      //        return UploadImageResponseDTO.builder()
      //                .imageCode(image.getImageCode())
      //                .status(ImageProcessingStatus.PENDING.name())
      //                .trackingUrl("/api/v1/images/" + image.getId() + "/status")
      //                .message("Image queued for processing")
      //                .build();
      //    }


    // AFTER — updated signature + passes request to createPendingImageRecord
    @Transactional
    public UploadImageResponseDTO queueImageProcessing(
            MultipartFile file,
            UploadImageRequest request,   // ← String metadata replaced with typed DTO
            String userId) throws ValidationException {

        log.info("[UPLOAD-START] user={}, filename={}, size={}", userId, file.getOriginalFilename(), file.getSize());

        // 1. VALIDATE
        validateUploadRequest(file);

        // 2. PRE-REGISTER — PENDING, with full metadata
        SatelliteImage image = createPendingImageRecord(file, request);  // ← now passes request
        log.info("[UPLOAD-REGISTERED] imageCode={}, status=PENDING", image.getImageCode());

        // 3. ASYNC BACKGROUND PROCESS
        processImageAsync(image, file);

        // 4. IMMEDIATE RESPONSE — client polls status endpoint
        return UploadImageResponseDTO.builder()
                .imageCode(image.getImageCode())
                .status(ImageProcessingStatus.PENDING.name())
                .trackingUrl("/api/v1/images/" + image.getId() + "/status")
                .message("Image queued for processing")
                .build();
    }


    /**
     * Runs in background (executor: imageProcessingExecutor).
     * Multi-step pipeline with comprehensive logging at each stage
     */
    @Async("imageProcessingExecutor")
    protected void processImageAsync(SatelliteImage image, MultipartFile file) {
        String imageCode     = image.getImageCode();
        String correlationId = UUID.randomUUID().toString();
        long pipelineStart   = System.currentTimeMillis();

        Path tempRaw = null;
        Path tempCog = null;

        log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
        log.info("║ [PROCESSING-PIPELINE-START] Async image processing pipeline initiated        ║");
        log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
        log.info("║ Image Code     : {}", padRight(imageCode, 63));
        log.info("║ Correlation ID : {}", padRight(correlationId, 63));
        log.info("║ Original File  : {}", padRight(file.getOriginalFilename(), 63));
        log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");

        try {
            // mark PROCESSING
            image.setStatus(ImageProcessingStatus.PROCESSING.name());
            imageRepository.save(image);
            log.info("✓ STEP 1/9: Status updated to PROCESSING");

            // STEP 1: save raw upload to temp disk
            tempRaw = saveTempFile(file, imageCode);
            long step1Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 2/9: Temp file saved ({} ms)", step1Time);
            log.debug("  File: {}", tempRaw.toAbsolutePath());

            // STEP 2: extract metadata & footprint from GDAL
            JsonNode gdalJson = gdalService.runGdalInfoJson(tempRaw);
            long step2Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 3/9: GDAL metadata extracted ({} ms)", (step2Time - step1Time));

            // ✅ CHANGE 1: Extract real EPSG — replaces hardcoded 4326
            int epsgCode = gdalService.extractEpsgCode(gdalJson);
            image.setCrsEpsg(epsgCode);

            Polygon footprint = gdalService.buildFootprintFromGdalJson(gdalJson);
            image.setFootprint(footprint);
            long step3Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 4/9: Footprint polygon built ({} ms)", (step3Time - step2Time));
            log.debug("  Bounds - X: [{}, {}] Y: [{}, {}]",
                    footprint.getEnvelopeInternal().getMinX(),
                    footprint.getEnvelopeInternal().getMaxX(),
                    footprint.getEnvelopeInternal().getMinY(),
                    footprint.getEnvelopeInternal().getMaxY());

            // STEP 3: convert to COG
            tempCog = Path.of(tempDirectory, imageCode + "_cog.tif");
            gdalService.convertToCog(tempRaw, tempCog);
            long step4Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 5/9: COG conversion complete ({} ms)", (step4Time - step3Time));
            log.debug("  COG File: {}", tempCog.toAbsolutePath());

            // STEP 4: upload RAW to MinIO
            String rawObjectPath = "raw/" + imageCode + "/" + file.getOriginalFilename();
            uploadToMinioWithRetry(
                    rawBucket,
                    rawObjectPath,
                    tempRaw,
                    file.getContentType() != null ? file.getContentType() : "application/octet-stream"
            );
            image.setRawObjectPath(rawObjectPath);
            long step5Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 6/9: Raw image uploaded to MinIO ({} ms)", (step5Time - step4Time));
            log.debug("  Path: {}", rawObjectPath);

            // STEP 5: upload COG to MinIO
            String cogObjectPath = "cog/" + imageCode + "/processed.tif";
            uploadToMinioWithRetry(
                    cogBucket,
                    cogObjectPath,
                    tempCog,
                    "image/tiff"
            );
            image.setCogObjectPath(cogObjectPath);
            long step6Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 7/9: COG uploaded to MinIO ({} ms)", (step6Time - step5Time));
            log.debug("  Path: {}", cogObjectPath);

            // STEP 6: copy COG to GeoServer shared directory
            Path sharedCogPath = copyToGeoServerDirectory(tempCog, imageCode);
            long step7Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 8/9: COG copied to GeoServer shared dir ({} ms)", (step7Time - step6Time));
            log.debug("  Path: {}", sharedCogPath.toAbsolutePath());

            // STEP 7: mark PROCESSING_COMPLETE before publish
            image.setStatus(ImageProcessingStatus.PROCESSING_COMPLETE.name());
            imageRepository.save(image);
            long step8Time = System.currentTimeMillis() - pipelineStart;
            log.info("✓ STEP 9/9: Database saved with PROCESSING_COMPLETE status ({} ms)", (step8Time - step7Time));

            // STEP 8: publish to GeoServer with retry
            String fileUrl = "file:" + sharedCogPath.toAbsolutePath().toString().replace("\\", "/");
            publishToGeoServerWithRetry(image, imageCode, fileUrl, correlationId);
            
            long totalTime = System.currentTimeMillis() - pipelineStart;
            log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
            log.info("║ [PROCESSING-PIPELINE-SUCCESS] Image processing completed successfully       ║");
            log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
            log.info("║ Image Code     : {}", padRight(imageCode, 63));
            log.info("║ Final Status   : PUBLISHED ✓");
            log.info("║ Total Duration : {} ms", padRight(String.valueOf(totalTime), 63));
            log.info("║ Layer Name     : {}:{}", "satellite-portal", imageCode);
            log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");

        } catch (Exception ex) {
            long totalTime = System.currentTimeMillis() - pipelineStart;
            log.error("╔═══════════════════════════════════════════════════════════════════════════════╗");
            log.error("║ [PROCESSING-PIPELINE-FAILED] Pipeline execution failed                      ║");
            log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
            log.error("║ Image Code     : {}", padRight(imageCode, 63));
            log.error("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));
            log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));
            log.error("║ Total Duration : {} ms", padRight(String.valueOf(totalTime), 63));
            log.error("║ Stack Trace:");
            log.error(ex.getMessage(), ex);
            log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");

            try {
                image.setStatus(ImageProcessingStatus.FAILED.name());
                imageRepository.save(image);
                log.error("║ Status Updated : FAILED");
                
                attemptRollback(image);
                log.error("║ Rollback       : COMPLETED");
            } catch (Exception rollbackEx) {
                log.error("║ Rollback       : FAILED");
                log.error("║ Rollback Error : {}", rollbackEx.getMessage());
                log.error(rollbackEx.getMessage(), rollbackEx);
            }
            
            log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");
        } finally {
            cleanupTempFiles(tempRaw, tempCog);
        }
    }

    // ─────────────────────────── Helpers ───────────────────────────

    private void validateUploadRequest(MultipartFile file) throws ValidationException {
        if (file == null || file.isEmpty()) {
            throw new ValidationException("File cannot be empty");
        }
        if (file.getSize() > maxFileSize) {
            throw new ValidationException(
                    String.format("File size (%d bytes) exceeds maximum (%d bytes)",
                            file.getSize(), maxFileSize)
            );
        }
        if (file.getOriginalFilename() == null) {
            throw new ValidationException("File must have a name");
        }
        if (!validationService.isValidFileExtension(file.getOriginalFilename())) {
            throw new ValidationException("Invalid file format. Allowed: .tif, .tiff, .jp2, .nitf");
        }
        log.debug("File validation passed: {}", file.getOriginalFilename());
    }

//    @Transactional
//    private SatelliteImage createPendingImageRecord(MultipartFile file) {
//        SatelliteImage image = new SatelliteImage();
//        image.setImageCode("IMG-" + UUID.randomUUID());
//        image.setStatus(ImageProcessingStatus.PENDING.name());
//        // additional metadata (title, satelliteName, sensorName, etc.) can be mapped here later
//        return imageRepository.save(image);
//    }


    @Transactional
    private SatelliteImage createPendingImageRecord(MultipartFile file, UploadImageRequest request) {
        SatelliteImage image = new SatelliteImage();

        // --- Identity & status ---
        image.setImageCode("IMG-" + UUID.randomUUID());
        image.setStatus(ImageProcessingStatus.PENDING.name());

        // --- All metadata fields from UploadImageRequest ---
        image.setTitle(request.getTitle());
        image.setSensorName(request.getSensorName());
        image.setSatelliteName(request.getSatelliteName());
        image.setProcessingLevel(request.getProcessingLevel());
        image.setAcquisitionDate(request.getAcquisitionDate());
        image.setCloudCover(request.getCloudCover());
        image.setResolutionM(request.getResolutionM());

        // --- Timestamps (also handled by @PrePersist, explicit here for clarity) ---
        image.setCreatedAt(LocalDateTime.now());
        image.setUpdatedAt(LocalDateTime.now());

        // Fields NOT set here (populated later by processImageAsync):
        // crsEpsg, footprint, rawObjectPath, cogObjectPath,
        // thumbnailPath, geoserverLayerName, geoserverWmsUrl, geoserverWmtsUrl

        return imageRepository.save(image);
    }

    private Path saveTempFile(MultipartFile file, String imageCode) throws Exception {
        Path tempDir = Files.createDirectories(Path.of(tempDirectory));
        Path tempFile = tempDir.resolve(imageCode + "_" + System.currentTimeMillis() + ".tmp");
        file.transferTo(tempFile);
        return tempFile;
    }

    private void uploadToMinioWithRetry(
            String bucket,
            String objectPath,
            Path file,
            String contentType
    ) {
        for (int attempt = 1; attempt <= minioRetryAttempts; attempt++) {
            try {
                log.info("MinIO upload attempt {}/{}: {}", attempt, minioRetryAttempts, objectPath);
                try (InputStream stream = Files.newInputStream(file)) {
                    minioService.upload(bucket, objectPath, stream, Files.size(file), contentType);
                }
                log.info("MinIO upload success: {}", objectPath);
                return;
            } catch (Exception ex) {
                log.warn("MinIO upload attempt {} failed: {}", attempt, ex.getMessage());
                if (attempt < minioRetryAttempts) {
                    long delayMs = (long) Math.pow(2, attempt) * 1000L;
                    try {
                        Thread.sleep(delayMs);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new ImageProcessingException("MinIO upload interrupted", ie);
                    }
                } else {
                    throw new ImageProcessingException(
                            "MinIO upload failed after " + minioRetryAttempts + " attempts: " + ex.getMessage(), ex);
                }
            }
        }
    }

    private Path copyToGeoServerDirectory(Path cogFile, String imageCode) throws Exception {
        Path targetDir = Files.createDirectories(Path.of(sharedDataDir, "cogs", imageCode));
        Path targetFile = targetDir.resolve("processed.tif");
        Files.copy(cogFile, targetFile, java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        log.info("COG copied to GeoServer shared dir: {}", targetFile);
        return targetFile;
    }

    private void publishToGeoServerWithRetry(
            SatelliteImage image,
            String imageCode,
            String cogFileUrl,
            String correlationId
    ) {
        for (int attempt = 1; attempt <= geoServerRetryAttempts; attempt++) {
            try {
                log.info("GeoServer publish attempt {}/{} correlationId={}",
                        attempt, geoServerRetryAttempts, correlationId);

                geoServerService.publishCogLayer(image, cogFileUrl);

                image.setGeoserverLayerName("satellite-portal:" + imageCode);
                image.setGeoserverWmsUrl(geoServerService.buildWmsUrl(image.getGeoserverLayerName()));
                image.setGeoserverWmtsUrl(geoServerService.buildWmtsUrl());
                image.setStatus(ImageProcessingStatus.PUBLISHED.name());
                imageRepository.save(image);

                log.info("GeoServer publish SUCCESS: imageCode={} correlationId={}",
                        imageCode, correlationId);
                return;
            } catch (Exception ex) {
                log.warn("GeoServer publish attempt {} failed: {}", attempt, ex.getMessage());
                if (attempt < geoServerRetryAttempts) {
                    long delayMs = (long) Math.pow(2, attempt) * 1000L;
                    try {
                        Thread.sleep(delayMs);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
        }

        log.error("GeoServer publish FAILED after {} attempts for imageCode={}",
                geoServerRetryAttempts, imageCode);
        image.setStatus(ImageProcessingStatus.PUBLISHED_FAILED.name());
        imageRepository.save(image);
    }

    private void cleanupTempFiles(Path... files) {
        for (Path file : files) {
            if (file == null) continue;
            try {
                Files.deleteIfExists(file);
            } catch (Exception ex) {
                log.warn("Failed to delete temp file {}: {}", file, ex.getMessage());
            }
        }
    }

    private void attemptRollback(SatelliteImage image) {
        try {
            if (image.getRawObjectPath() != null) {
                minioService.deleteObject(rawBucket, image.getRawObjectPath());
                log.info("Rollback: deleted raw MinIO object {}", image.getRawObjectPath());
            }
            if (image.getCogObjectPath() != null) {
                minioService.deleteObject(cogBucket, image.getCogObjectPath());
                log.info("Rollback: deleted COG MinIO object {}", image.getCogObjectPath());
            }
        } catch (Exception ex) {
            log.error("Rollback cleanup failed: {}", ex.getMessage(), ex);
        }
    }

    // ===== HELPER METHODS =====
    private String padRight(String s, int n) {
        if (s == null) s = "N/A";
        return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
    }
}



========================================================================================================================
FILE PATH: Orbit_API/catalog/service/ImageMetadataService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

public class ImageMetadataService {
}


========================================================================================================================
FILE PATH: Orbit_API/catalog/service/ImageStatusService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.util.Optional;
import java.util.UUID;

@Slf4j
@Service
public class ImageStatusService {

    private final SatelliteImageRepository imageRepository;

    public ImageStatusService(SatelliteImageRepository imageRepository) {
        this.imageRepository = imageRepository;
    }

    public SatelliteImage getImageStatus(UUID imageId) {
        Optional<SatelliteImage> image = imageRepository.findById(imageId);
        if (image.isEmpty()) {
            log.warn("Image not found: {}", imageId);
            return null;
        }
        return image.get();
    }

    public ImageProcessingStatus getCurrentStatus(UUID imageId) {
        SatelliteImage image = getImageStatus(imageId);
        if (image == null) return null;
        String statusString = image.getStatus();
        if (statusString == null) return null;
        
        try {
            return ImageProcessingStatus.valueOf(statusString);
        } catch (IllegalArgumentException e) {
            log.warn("Unknown status value: {} for image: {}", statusString, imageId);
            return null;
        }
    }

    public int getProgress(UUID imageId) {
        ImageProcessingStatus status = getCurrentStatus(imageId);
        if (status == null) return 0;

        switch (status) {
            case PENDING:
                return 0;
            case PROCESSING:
                return 50;
            case PROCESSING_COMPLETE:
                return 75;
            case PUBLISHED:
                return 100;
            case PUBLISHED_FAILED:
                return 90;
            case FAILED:
                return -1;
            default:
                return 0;
        }
    }

    public String getCurrentStep(UUID imageId) {
        ImageProcessingStatus status = getCurrentStatus(imageId);
        if (status == null) return "Unknown";

        switch (status) {
            case PENDING:
                return "Queued for processing";
            case PROCESSING:
                return "Processing image";
            case PROCESSING_COMPLETE:
                return "Publishing to GeoServer";
            case PUBLISHED:
                return "Complete";
            case PUBLISHED_FAILED:
                return "Publishing failed - waiting for retry";
            case FAILED:
                return "Failed - manual intervention required";
            default:
                return "Unknown";
        }
    }
}

========================================================================================================================
FILE PATH: Orbit_API/catalog/service/ImageValidationService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

import com.Orbit_API.exception.ValidationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

/**
* PRODUCTION Image Validation Service
*
* Validates:
* - File format/extension
* - File integrity (magic bytes)
* - Geospatial format compatibility
    */
    @Slf4j
    @Service
    public class ImageValidationService {

private static final Set<String> ALLOWED_EXTENSIONS = new HashSet<>(Arrays.asList(
".tif", ".tiff", ".geotiff",
".jp2", ".jpeg2000",
".nitf", ".ntf",
".env", ".bil", ".bip", ".bsq"
));

private static final Set<String> ALLOWED_MIMETYPES = new HashSet<>(Arrays.asList(
"image/tiff",
"image/geotiff",
"image/jp2",
"image/jpeg2000",
"application/octet-stream" // For NITF, ENVI
));

/**
    * Check if file extension is allowed
      */
      public boolean isValidFileExtension(String filename) {
      if (filename == null || filename.isEmpty()) {
      return false;
      }

      String lowerName = filename.toLowerCase();
      return ALLOWED_EXTENSIONS.stream().anyMatch(lowerName::endsWith);
      }

/**
    * Validate file format by checking magic bytes (file signature)
      */
      public boolean validateFileMagicBytes(byte[] fileHeader) {
      if (fileHeader == null || fileHeader.length < 4) {
      return false;
      }

      // GeoTIFF: starts with "II*\0" (little endian) or "MM\0*" (big endian)
      if ((fileHeader[0] == 0x49 && fileHeader[1] == 0x49 &&
      fileHeader[2] == 0x2A && fileHeader[3] == 0x00) ||
      (fileHeader[0] == 0x4D && fileHeader[1] == 0x4D &&
      fileHeader[2] == 0x00 && fileHeader[3] == 0x2A)) {
      return true;
      }

      // JPEG2000: starts with 0xFF4F
      if (fileHeader[0] == (byte) 0xFF && fileHeader[1] == 0x4F) {
      return true;
      }

      // NITF: starts with "NITF"
      if (fileHeader.length >= 4 &&
      fileHeader[0] == 'N' && fileHeader[1] == 'I' &&
      fileHeader[2] == 'T' && fileHeader[3] == 'F') {
      return true;
      }

      return false;
      }

/**
    * Validate image dimensions are reasonable
      */
      public boolean validateImageDimensions(long width, long height, long pixelCount) {
      // Must have at least 1x1 pixels
      if (width < 1 || height < 1) {
      return false;
      }

      // Maximum reasonable dimension (prevent overflow): 100,000 x 100,000
      if (width > 100_000 || height > 100_000) {
      return false;
      }

      // Total pixels check (prevent memory overflow)
      // Max 1 billion pixels (e.g., 31,623 x 31,623)
      if (pixelCount > 1_000_000_000) {
      return false;
      }

      return true;
      }

/**
    * Validate geospatial bounds are realistic
      */
      public boolean validateGeospatialBounds(double minX, double maxX, double minY, double maxY) {
      // For geographic coordinates (EPSG:4326)
      if (minX >= maxX || minY >= maxY) {
      return false;
      }

      // Longitude: -180 to 180
      if (minX < -180 || maxX > 180) {
      return false;
      }

      // Latitude: -90 to 90
      if (minY < -90 || maxY > 90) {
      return false;
      }

      return true;
      }

/**
    * Validate cloud cover percentage
      */
      public boolean validateCloudCover(Double cloudCover) {
      return cloudCover != null && cloudCover >= 0 && cloudCover <= 100;
      }

/**
    * Validate spatial resolution in meters
      */
      public boolean validateResolution(Double resolutionM) {
      // Resolution must be positive and reasonable (0.1m to 10,000m)
      return resolutionM != null && resolutionM > 0.1 && resolutionM < 10_000;
      }
      }

========================================================================================================================
FILE PATH: Orbit_API/catalog/service/MinioRetryService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

public class MinioRetryService {
}


========================================================================================================================
FILE PATH: Orbit_API/catalog/service/SatelliteImageService.java
========================================================================================================================

package com.Orbit_API.catalog.service;

import java.util.List;
import java.util.UUID;

import com.Orbit_API.catalog.dto.SearchResultDTO;
import com.Orbit_API.catalog.dto.ImageSearchRequestDTO;

import com.Orbit_API.exception.ValidationException;
import org.springframework.web.multipart.MultipartFile;

import com.Orbit_API.catalog.dto.ImageResponse;
import com.Orbit_API.catalog.dto.ImageSearchRequest;
import com.Orbit_API.catalog.dto.UploadImageRequest;

public interface SatelliteImageService {
ImageResponse uploadAndProcess(UploadImageRequest request, MultipartFile file);
List<ImageResponse> searchByPolygon(ImageSearchRequest request);
ImageResponse getById(UUID id);
String getDownloadUrl(UUID id);
// New — full paginated search with all filters
SearchResultDTO searchByPolygonFull(ImageSearchRequestDTO request) throws ValidationException;
void deleteImage(UUID id);
}


========================================================================================================================
FILE PATH: Orbit_API/catalog/service/SatelliteImageServiceImpl.java
========================================================================================================================

package com.Orbit_API.catalog.service;

import com.Orbit_API.catalog.dto.ImageSearchRequestDTO;
import com.Orbit_API.catalog.dto.SearchResultDTO;
import com.Orbit_API.exception.ValidationException;
import com.fasterxml.jackson.databind.JsonNode;
import com.Orbit_API.catalog.dto.ImageResponse;
import com.Orbit_API.catalog.dto.ImageSearchRequest;
import com.Orbit_API.catalog.dto.UploadImageRequest;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.geoserver.GeoServerRestService;
import com.Orbit_API.processing.GdalProcessingService;
import com.Orbit_API.storage.MinioStorageService;
import org.locationtech.jts.geom.Polygon;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import com.Orbit_API.exception.NotFoundException;
import org.springframework.transaction.annotation.Transactional;
import lombok.extern.slf4j.Slf4j;


import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
public class SatelliteImageServiceImpl implements SatelliteImageService {

    private final SatelliteImageRepository repository;
    private final MinioStorageService minioStorageService;
    private final GdalProcessingService gdalProcessingService;
    private final GeoServerRestService geoServerRestService;

    @Value("${orbitview.shared-data-dir}")
    private String sharedDataDir;

    @Value("${minio.bucket-raw}")
    private String rawBucket;

    @Value("${minio.bucket-cog}")
    private String cogBucket;

    public SatelliteImageServiceImpl(
            SatelliteImageRepository repository,
            MinioStorageService minioStorageService,
            GdalProcessingService gdalProcessingService,
            GeoServerRestService geoServerRestService) {
        this.repository = repository;
        this.minioStorageService = minioStorageService;
        this.gdalProcessingService = gdalProcessingService;
        this.geoServerRestService = geoServerRestService;
    }

    // =========================================================================
    // UPLOAD & PROCESS
    // =========================================================================

    @Override
    public ImageResponse uploadAndProcess(UploadImageRequest request, MultipartFile file) {
        try {
            minioStorageService.ensureBuckets();

            String originalName = file.getOriginalFilename();
            String imageCode = "IMG-" + UUID.randomUUID();

            // 1) Save uploaded file locally first
            Path tempRaw = Files.createTempFile("orbitview-raw-", "-" + originalName);
            file.transferTo(tempRaw);

            // 2) Read metadata from GDAL
            JsonNode gdalJson = gdalProcessingService.runGdalInfoJson(tempRaw);

            // 3) Convert to COG
            Path tempCog = Files.createTempFile("orbitview-cog-", ".tif");
            gdalProcessingService.convertToCog(tempRaw, tempCog);

            // 4) Extract real footprint from GDAL WGS84 extent
            Polygon footprint = gdalProcessingService.buildFootprintFromGdalJson(gdalJson);

            // 5) Upload raw file to MinIO
            String rawObjectPath = "raw/" + imageCode + "/" + originalName;
            try (InputStream rawStream = Files.newInputStream(tempRaw)) {
                minioStorageService.upload(
                        rawBucket,
                        rawObjectPath,
                        rawStream,
                        Files.size(tempRaw),
                        file.getContentType() != null ? file.getContentType() : "application/octet-stream"
                );
            }

            // 6) Upload COG to MinIO
            String cogObjectPath = "cog/" + imageCode + "/processed.tif";
            try (InputStream cogStream = Files.newInputStream(tempCog)) {
                minioStorageService.upload(
                        cogBucket,
                        cogObjectPath,
                        cogStream,
                        Files.size(tempCog),
                        "image/tiff"
                );
            }

            // 7) Copy COG into shared folder so GeoServer can read it
            Path sharedCogPath = copyCogToSharedFolder(imageCode, tempCog);

            // 8) Save image row in PostGIS
            SatelliteImage image = new SatelliteImage();
            image.setImageCode(imageCode);
            image.setTitle(request.getTitle());
            image.setSensorName(request.getSensorName());
            image.setSatelliteName(request.getSatelliteName());
            image.setProcessingLevel(request.getProcessingLevel());
            image.setAcquisitionDate(request.getAcquisitionDate());
            image.setCloudCover(request.getCloudCover());
            image.setResolutionM(request.getResolutionM());
            int epsgCode = gdalProcessingService.extractEpsgCode(gdalJson);
            image.setCrsEpsg(epsgCode);
            image.setFootprint(footprint);
            image.setRawObjectPath(rawObjectPath);
            image.setCogObjectPath(cogObjectPath);
            image.setStatus("PROCESSED");
            image = repository.save(image);

            // 9) Publish to GeoServer (reads from shared filesystem path)
            geoServerRestService.publishCogLayer(
                    image,
                    "file:" + sharedCogPath.toAbsolutePath().toString().replace("\\", "/")
            );

            // 10) Update GeoServer URLs in DB
            image.setGeoserverLayerName("satellite-portal:" + imageCode);
            image.setGeoserverWmsUrl(geoServerRestService.buildWmsUrl(image.getGeoserverLayerName()));
            image.setGeoserverWmtsUrl(geoServerRestService.buildWmtsUrl());
            image.setStatus("PUBLISHED");
            image = repository.save(image);

            return toResponse(image);

        } catch (Exception ex) {
            throw new RuntimeException("Image ingestion failed: " + ex.getMessage(), ex);
        }
    }

    // =========================================================================
    // SEARCH — updated to use the new 9-parameter repository method.
    // ImageSearchRequest only carries geoJsonPolygon, sensorName, maxCloudCover,
    // so new filters (satellite, minResolutionM, dateFrom, dateTo) are passed
    // as null — they are skipped by the IS NULL OR pattern in the query.
    // Default pagination: page 0, pageSize 20 (no pagination in this DTO).
    // =========================================================================

    @Override
    public List<ImageResponse> searchByPolygon(ImageSearchRequest request) {
        List<SatelliteImage> result = repository.searchByPolygon(
                request.getGeoJsonPolygon(),  // required
                request.getSensorName(),       // nullable — skipped if null
                null,                          // satellite     — not in ImageSearchRequest
                request.getMaxCloudCover(),    // nullable — skipped if null
                null,                          // minResolutionM — not in ImageSearchRequest
                null,                          // dateFrom       — not in ImageSearchRequest
                null,                          // dateTo         — not in ImageSearchRequest
                20,                            // default page size
                0                              // default offset (page 0)
        );

        return result.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
    }

    // =========================================================================
    // GET BY ID
    // =========================================================================

    @Override
    public ImageResponse getById(UUID id) {
        SatelliteImage image = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Image not found"));
        return toResponse(image);
    }

    // =========================================================================
    // DOWNLOAD URL
    // =========================================================================

    @Override
    public String getDownloadUrl(UUID id) {
        try {
            SatelliteImage image = repository.findById(id)
                    .orElseThrow(() -> new RuntimeException("Image not found"));
            return minioStorageService.createSignedDownloadUrl(
                    cogBucket,
                    image.getCogObjectPath(),
                    60
            );
        } catch (Exception ex) {
            throw new RuntimeException("Download URL generation failed: " + ex.getMessage(), ex);
        }
    }

    // =========================================================================
    // PRIVATE HELPERS
    // =========================================================================

    private Path copyCogToSharedFolder(String imageCode, Path tempCog) throws Exception {
        Path targetDir = Path.of(sharedDataDir, "cogs", imageCode);
        Files.createDirectories(targetDir);
        Path targetFile = targetDir.resolve("processed.tif");
        Files.copy(tempCog, targetFile, java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        return targetFile;
    }

    private ImageResponse toResponse(SatelliteImage image) {
        ImageResponse res = new ImageResponse();
        res.setId(image.getId());
        res.setImageCode(image.getImageCode());
        res.setTitle(image.getTitle());
        res.setSensorName(image.getSensorName());
        res.setSatelliteName(image.getSatelliteName());
        res.setProcessingLevel(image.getProcessingLevel());
        res.setAcquisitionDate(image.getAcquisitionDate());
        res.setCloudCover(image.getCloudCover());
        res.setResolutionM(image.getResolutionM());
        res.setGeoserverLayerName(image.getGeoserverLayerName());
        res.setGeoserverWmsUrl(image.getGeoserverWmsUrl());
        res.setGeoserverWmtsUrl(image.getGeoserverWmtsUrl());
        res.setThumbnailPath(image.getThumbnailPath());

        // Convert JTS Polygon → GeoJSON string for OpenLayers
        if (image.getFootprint() != null) {
            org.locationtech.jts.io.geojson.GeoJsonWriter writer =
                    new org.locationtech.jts.io.geojson.GeoJsonWriter();
            res.setFootprintGeoJson(writer.write(image.getFootprint()));
        } else {
            res.setFootprintGeoJson(null);
        }

        return res;
    }


// =========================================================================
// FULL PAGINATED SEARCH — uses ImageSearchRequestDTO with all filters
// =========================================================================

    @Override
    public SearchResultDTO searchByPolygonFull(ImageSearchRequestDTO request) throws ValidationException {

        // 1. Validate — polygon is mandatory
        if (request.getGeoJsonPolygon() == null || request.getGeoJsonPolygon().isBlank()) {
            throw new ValidationException("geoJsonPolygon must not be null or blank");
        }

        // 2. Resolve pagination — getPage()/getPageSize() use Builder.Default so never null
        int page     = request.getPage()     != null ? request.getPage()     : 0;
        int pageSize = request.getPageSize() != null ? request.getPageSize() : 20;
        int offset   = page * pageSize;

        // 3. Fetch page of results
        List<SatelliteImage> images = repository.searchByPolygon(
                request.getGeoJsonPolygon(),
                null,                       // sensorName — not in ImageSearchRequestDTO
                request.getSatellite(),
                request.getMaxCloudCover(),
                request.getMinResolutionM(),
                request.getDateFrom(),
                request.getDateTo(),
                pageSize,
                offset
        );

        // 4. Count total matching rows (same WHERE, no LIMIT/OFFSET)
        long totalCount = repository.countByPolygon(
                request.getGeoJsonPolygon(),
                null,                       // sensorName
                request.getSatellite(),
                request.getMaxCloudCover(),
                request.getMinResolutionM(),
                request.getDateFrom(),
                request.getDateTo()
        );

        // 5. Map entities → response DTOs (toResponse handles footprint GeoJSON)
        List<ImageResponse> responseList = images.stream()
                .map(this::toResponse)
                .collect(Collectors.toList());

        // 6. Build and return paginated wrapper
        return new SearchResultDTO(responseList, totalCount, page, pageSize);
    }

    @Value("${minio.bucket-thumbnails:Orbit_API-thumbnails}")
    private String thumbBucket;

    @Override
    @Transactional
    public void deleteImage(UUID id) {
        log.info("");
        log.info("[DELETE-START] Beginning full cleanup for image id={}", id);

        // 1. FIND ENTITY — throw 404 if not found
        SatelliteImage image = repository.findById(id)
                .orElseThrow(() -> new NotFoundException("Image not found with id: " + id));

        String imageCode = image.getImageCode();
        log.info("[DELETE] imageCode={}, status={}", imageCode, image.getStatus());

        // 2. DELETE RAW FILE from MinIO
        if (image.getRawObjectPath() != null) {
            try {
                minioStorageService.deleteObject(rawBucket, image.getRawObjectPath());
                log.info("[DELETE-MINIO-RAW] Deleted raw object: {}", image.getRawObjectPath());
            } catch (Exception ex) {
                log.warn("[DELETE-MINIO-RAW-WARN] Could not delete raw object '{}': {}",
                        image.getRawObjectPath(), ex.getMessage());
            }
        } else {
            log.debug("[DELETE-MINIO-RAW] rawObjectPath is null — skipping");
        }

        // 3. DELETE COG FILE from MinIO
        if (image.getCogObjectPath() != null) {
            try {
                minioStorageService.deleteObject(cogBucket, image.getCogObjectPath());
                log.info("[DELETE-MINIO-COG] Deleted COG object: {}", image.getCogObjectPath());
            } catch (Exception ex) {
                log.warn("[DELETE-MINIO-COG-WARN] Could not delete COG object '{}': {}",
                        image.getCogObjectPath(), ex.getMessage());
            }
        } else {
            log.debug("[DELETE-MINIO-COG] cogObjectPath is null — skipping");
        }

        // 4. DELETE THUMBNAIL from MinIO (optional — only if path is set)
        if (image.getThumbnailPath() != null) {
            try {
                minioStorageService.deleteObject(thumbBucket, image.getThumbnailPath());
                log.info("[DELETE-MINIO-THUMB] Deleted thumbnail: {}", image.getThumbnailPath());
            } catch (Exception ex) {
                log.warn("[DELETE-MINIO-THUMB-WARN] Could not delete thumbnail '{}': {}",
                        image.getThumbnailPath(), ex.getMessage());
            }
        } else {
            log.debug("[DELETE-MINIO-THUMB] thumbnailPath is null — skipping");
        }

        // 5. DELETE GEOSERVER LAYER (catch and log — do not block DB delete)
        if (image.getGeoserverLayerName() != null) {
            try {
                geoServerRestService.deleteLayer(imageCode);
                log.info("[DELETE-GEOSERVER] Layer deleted for imageCode={}", imageCode);
            } catch (Exception ex) {
                log.warn("[DELETE-GEOSERVER-WARN] Could not delete GeoServer layer for imageCode='{}': {}",
                        imageCode, ex.getMessage());
            }
        } else {
            log.debug("[DELETE-GEOSERVER] No geoserverLayerName set — skipping GeoServer cleanup");
        }

        // 6. DELETE FROM DATABASE
        repository.deleteById(id);
        log.info("[DELETE-DB] Entity deleted from database. imageCode={}, id={}", imageCode, id);
        log.info("[DELETE-COMPLETE] Full cleanup finished for imageCode={}", imageCode);
    }


}

========================================================================================================================
FILE PATH: Orbit_API/commom/HealthController.java
========================================================================================================================

package com.Orbit_API.commom;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/health")
public class HealthController {

    @GetMapping
    public String health() {
        return "OrbitView Backend Running Successfully";
    }
}

========================================================================================================================
FILE PATH: Orbit_API/config/AsyncConfig.java
========================================================================================================================

package com.Orbit_API.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "imageProcessingExecutor")
    public Executor imageProcessingExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(3);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("image-processing-");
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(60);
        executor.initialize();
        return executor;
    }
}

========================================================================================================================
FILE PATH: Orbit_API/config/GeoServerConfig.java
========================================================================================================================

package com.Orbit_API.config;


import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpRequest;
import org.springframework.http.client.ClientHttpRequestExecution;
import org.springframework.http.client.ClientHttpRequestInterceptor;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.List;

/**
* GeoServerConfig — configures a RestTemplate bean pre-wired with:
*   - HTTP Basic Authentication on every outgoing request
*   - Connection timeout : 10 seconds
*   - Read (socket) timeout: 30 seconds
*
* Consumed by GeoServerRestService via @Qualifier("geoServerRestTemplate").
* Credentials are read from application.yml under geoserver.username / geoserver.password.
  */
  @Slf4j
  @Configuration
  public class GeoServerConfig {

  @Value("${geoserver.username:admin}")
  private String username;

  @Value("${geoserver.password:geoserver}")
  private String password;

  /**
    * RestTemplate with Basic Auth interceptor and explicit timeouts.
    *
    * The interceptor computes the Base64 token once at bean construction
    * time (credentials are static per deployment), then stamps every
    * outgoing request with  Authorization: Basic <token>  so that
    * GeoServerRestService never has to touch auth headers manually.
      */
      @Bean(name = "geoServerRestTemplate")
      public RestTemplate geoServerRestTemplate() {

      // ── 1. Timeouts via SimpleClientHttpRequestFactory ─────────────────
      SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
      factory.setConnectTimeout(10_000);   // 10 s — fail fast if GeoServer is down
      factory.setReadTimeout(30_000);      // 30 s — COG publish can be slow

      RestTemplate restTemplate = new RestTemplate(factory);

      // ── 2. Pre-compute the static Basic Auth token ─────────────────────
      String credentials = username + ":" + password;
      String encoded = Base64.getEncoder()
      .encodeToString(credentials.getBytes(StandardCharsets.UTF_8));
      String authorizationHeader = "Basic " + encoded;

      log.info("[GEOSERVER-CONFIG] RestTemplate initialised");
      log.info("[GEOSERVER-CONFIG]   Username           : {}", username);
      log.info("[GEOSERVER-CONFIG]   Connect timeout    : 10 s");
      log.info("[GEOSERVER-CONFIG]   Read timeout       : 30 s");
      log.info("[GEOSERVER-CONFIG]   Auth header        : Basic ****** (encoded)");

      // ── 3. Interceptor — stamps every request with the header ───────────
      ClientHttpRequestInterceptor basicAuthInterceptor =
      new GeoServerBasicAuthInterceptor(authorizationHeader);

      restTemplate.setInterceptors(List.of(basicAuthInterceptor));

      return restTemplate;
      }

  /**
    * Stateless interceptor that injects a pre-computed Authorization header.
    * Declared as a named static class so it is independently testable.
      */
      static class GeoServerBasicAuthInterceptor implements ClientHttpRequestInterceptor {

      private final String authorizationHeader;

      GeoServerBasicAuthInterceptor(String authorizationHeader) {
      this.authorizationHeader = authorizationHeader;
      }

      @Override
      public ClientHttpResponse intercept(
      HttpRequest request,
      byte[] body,
      ClientHttpRequestExecution execution) throws IOException {

           // Only add header if not already present (allows manual override in tests)
           if (!request.getHeaders().containsKey("Authorization")) {
               request.getHeaders().add("Authorization", authorizationHeader);
           }
           return execution.execute(request, body);
      }
      }
      }


========================================================================================================================
FILE PATH: Orbit_API/config/LoggingConfig.java
========================================================================================================================

package com.Orbit_API.config;

import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.util.UUID;

/**
* Logging Configuration
*
* Implements request tracing with correlation IDs:
* - Generates unique ID for each request
* - Stores in MDC for logging
* - Returns in response header (X-Correlation-ID)
* - Enables distributed tracing across services
    */
    @Slf4j
    @Configuration
    public class LoggingConfig implements WebMvcConfigurer {

@Override
public void addInterceptors(InterceptorRegistry registry) {
registry.addInterceptor(new CorrelationIdInterceptor());
}

/**
    * Request Interceptor for Correlation ID Management
    *
    * PreHandle:  Generate/extract correlation ID, store in MDC
    * PostHandle: Add to response header
    * AfterCompletion: Clean up MDC
      */
      @Slf4j
      public static class CorrelationIdInterceptor implements HandlerInterceptor {

      private static final String CORRELATION_ID_HEADER = "X-Correlation-ID";
      private static final String CORRELATION_ID_MDC = "correlationId";
      private static final String USER_ID_MDC = "userId";

      /**
        * Executed before the handler
        * Extract or generate correlation ID
          */
          @Override
          public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
          long startTime = System.currentTimeMillis();

          // Get or generate correlation ID
          String correlationId = request.getHeader(CORRELATION_ID_HEADER);
          if (correlationId == null || correlationId.isEmpty()) {
          correlationId = UUID.randomUUID().toString();
          }

          // Get user ID from Authorization header or Security context (if available)
          String userId = request.getHeader("X-User-ID");
          if (userId == null || userId.isEmpty()) {
          userId = "ANONYMOUS";
          }

          // Store in MDC for all logs in this thread
          MDC.put(CORRELATION_ID_MDC, correlationId);
          MDC.put(USER_ID_MDC, userId);

          // Store timestamps for duration calculation
          request.setAttribute("_START_TIME", startTime);
          request.setAttribute("_CORRELATION_ID", correlationId);

          // Log request start
          log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
          log.info("║ [REQUEST-START] Incoming HTTP request                                        ║");
          log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
          log.info("║ Correlation ID : {}", padRight(correlationId, 63));
          log.info("║ User ID        : {}", padRight(userId, 63));
          log.info("║ Method         : {}", padRight(request.getMethod(), 63));
          log.info("║ URI            : {}", padRight(request.getRequestURI(), 63));
          log.info("║ Query String   : {}", padRight(request.getQueryString() != null ? request.getQueryString() : "N/A", 63));
          log.info("║ Remote IP      : {}", padRight(getClientIp(request), 63));
          log.info("║ User Agent     : {}", padRight(request.getHeader("User-Agent"), 63));
          log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");

          return true;
          }

      /**
        * Executed after handler returns but before response is sent
        * Add correlation ID to response header
          */
          @Override
          public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
          org.springframework.web.servlet.ModelAndView modelAndView) {
          String correlationId = (String) request.getAttribute("_CORRELATION_ID");
          if (correlationId != null) {
          response.addHeader(CORRELATION_ID_HEADER, correlationId);
          }
          }

      /**
        * Executed after response is sent
        * Log request completion and cleanup MDC
          */
          @Override
          public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
          Object handler, Exception ex) {
          long startTime = (long) request.getAttribute("_START_TIME");
          long duration = System.currentTimeMillis() - startTime;
          int status = response.getStatus();
          String correlationId = MDC.get(CORRELATION_ID_MDC);

          log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
          log.info("║ [REQUEST-COMPLETE] HTTP request completed                                   ║");
          log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
          log.info("║ Correlation ID : {}", padRight(correlationId, 63));
          log.info("║ Status Code    : {}", padRight(String.valueOf(status), 63));
          log.info("║ Duration       : {} ms", padRight(String.valueOf(duration), 63));
          log.info("║ Content Type   : {}", padRight(response.getContentType(), 63));

          if (ex != null) {
          log.error("║ Exception      : {}", padRight(ex.getClass().getSimpleName(), 63));
          log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));
          }

          log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");

          // Clear MDC to prevent memory leaks
          MDC.clear();
          }
          }

// ===== HELPER METHODS =====

/**
    * Extract client IP address from request headers
    * Handles X-Forwarded-For header (for reverse proxies)
    *
    * @param request HTTP request
    * @return Client IP address
      */
      private static String getClientIp(HttpServletRequest request) {
      String xForwardedFor = request.getHeader("X-Forwarded-For");
      if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
      // X-Forwarded-For can contain multiple IPs, get the first one
      return xForwardedFor.split(",")[0].trim();
      }

      String xRealIp = request.getHeader("X-Real-IP");
      if (xRealIp != null && !xRealIp.isEmpty()) {
      return xRealIp;
      }

      return request.getRemoteAddr();
      }

private static String padRight(String s, int n) {
if (s == null) s = "N/A";
return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
}
}

========================================================================================================================
FILE PATH: Orbit_API/config/MinioConfig.java
========================================================================================================================

package com.Orbit_API.config;

import io.minio.MinioClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MinioConfig {

    @Bean
    public MinioClient minioClient(
            @Value("${minio.url}") String url,
            @Value("${minio.access-key}") String accessKey,
            @Value("${minio.secret-key}") String secretKey
    ) {
        return MinioClient.builder()
                .endpoint(url)
                .credentials(accessKey, secretKey)
                .build();
    }
}


========================================================================================================================
FILE PATH: Orbit_API/config/WebConfig.java
========================================================================================================================

package com.Orbit_API.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.Set;

/**
* WebConfig — MVC-layer CORS configuration for OrbitView.
*
* Works alongside SecurityConfig which registers the same origins
* at the Spring Security filter chain level. Both layers must agree —
* Spring Security's CorsFilter runs first and WebMvcConfigurer fills
* in for non-security routes (e.g., /api/v1/health).
*
* Origins are resolved with this priority:
*   1. ${cors.allowed-origins} from application.yml  — overrides all (production/staging)
*   2. Hardcoded dev defaults: http://localhost:3000 and http://localhost:4200
* Both are always merged so local development always works even when
* application.yml is configured for a different environment.
  */
  @Slf4j
  @Configuration
  public class WebConfig implements WebMvcConfigurer {

  /**
    * Reads allowed origins from application.yml.
    * Default value is http://localhost:3000 so the app starts without
    * any yml configuration in local development.
    *
    * In application.yml (optional — add for non-dev environments):
    *   cors:
    *     allowed-origins: https://orbitview.yourdomain.com
    *
    * Multiple origins comma-separated:
    *   cors:
    *     allowed-origins: https://app.example.com,https://admin.example.com
  */
  @Value("${cors.allowed-origins:http://localhost:3000}")
  private String allowedOriginsConfig;

  // Always-allowed dev origins — merged with the yml value
  private static final String DEV_ORIGIN_REACT  = "http://localhost:3000"; // React (CRA / Vite)
  private static final String DEV_ORIGIN_ANGULAR = "http://localhost:4200"; // Angular (if needed)

  @Override
  public void addCorsMappings(CorsRegistry registry) {

       // ── Merge all allowed origins ──────────────────────────────────────
       // LinkedHashSet preserves insertion order and deduplicates.
       Set<String> origins = new LinkedHashSet<>();

       // 1. Add hardcoded dev defaults first
       origins.add(DEV_ORIGIN_REACT);
       origins.add(DEV_ORIGIN_ANGULAR);

       // 2. Add any origins from application.yml (comma-separated list supported)
       if (allowedOriginsConfig != null && !allowedOriginsConfig.isBlank()) {
           Arrays.stream(allowedOriginsConfig.split(","))
                   .map(String::trim)
                   .filter(s -> !s.isEmpty())
                   .forEach(origins::add);
       }

       String[] resolvedOrigins = origins.toArray(new String[0]);

       log.info("[CORS] WebConfig CORS mapping registered");
       log.info("[CORS]   Path pattern     : /api/**");
       log.info("[CORS]   Allowed origins  : {}", Arrays.toString(resolvedOrigins));
       log.info("[CORS]   Allowed methods  : GET, POST, PUT, DELETE, OPTIONS");
       log.info("[CORS]   Allow credentials: true");
       log.info("[CORS]   Max age (seconds): 3600");

       registry.addMapping("/api/**")
               .allowedOrigins(resolvedOrigins)
               .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
               .allowedHeaders("*")
               .allowCredentials(true)
               .maxAge(3600);
  }
  }

========================================================================================================================
FILE PATH: Orbit_API/config/security/JwtAuthenticationFilter.java
========================================================================================================================

package com.Orbit_API.config.security;

public class JwtAuthenticationFilter {
}


========================================================================================================================
FILE PATH: Orbit_API/config/security/JwtTokenProvider.java
========================================================================================================================

package com.Orbit_API.config.security;

public class JwtTokenProvider {
}


========================================================================================================================
FILE PATH: Orbit_API/config/security/KeycloakProperties.java
========================================================================================================================

package com.Orbit_API.config.security;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "keycloak")
public class KeycloakProperties {
private String realm;
private String authServerUrl;
private String sslRequired;
private String resource;
private String bearerOnly;
private RealmConfig realmConfig;

    @Data
    public static class RealmConfig {
        private String publicKey;
    }
}


========================================================================================================================
FILE PATH: Orbit_API/config/security/SecurityConfig.java
========================================================================================================================

package com.Orbit_API.config.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(authz -> authz
                        .requestMatchers("/api/v1/health/**").permitAll()
                        .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                        .requestMatchers("/api/v1/images/upload").permitAll()
                        .requestMatchers("/api/v1/images/search", "/api/v1/images/**").permitAll()
                        .requestMatchers("/api/v1/exports/**").permitAll()
                        .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated()
                )
                .httpBasic(httpBasic -> httpBasic.disable())
                .csrf(csrf -> csrf.disable())
                .cors(cors -> cors.configurationSource(corsConfigurationSource()));

        return http.build();
    }

    @Bean
    public UrlBasedCorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("http://localhost:3000", "http://localhost:4200"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}

========================================================================================================================
FILE PATH: Orbit_API/exception/ApiExceptionHandler.java
========================================================================================================================

package com.Orbit_API.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handle(Exception ex) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of(
                        "error", ex.getMessage()
                ));
    }
}

========================================================================================================================
FILE PATH: Orbit_API/exception/GlobalExceptionHandler.java
========================================================================================================================

package com.Orbit_API.exception;

import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;




import java.time.LocalDateTime;
import java.util.*;

/**
* Global Exception Handler
*
* Handles all exceptions across the application:
* - Validation errors (400)
* - Image processing errors (500)
* - Not found errors (404)
* - General runtime exceptions (500)
*
* All exceptions are logged with correlation ID for tracing
  */
  @Slf4j
  @RestControllerAdvice
  public class GlobalExceptionHandler {

  /**
    * Handle validation errors from @Valid/@Validated
    * Returns 400 Bad Request
      */
      @ExceptionHandler(MethodArgumentNotValidException.class)
      public ResponseEntity<?> handleValidationError(MethodArgumentNotValidException ex) {
      String correlationId = MDC.get("correlationId");

      log.warn("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.warn("║ [VALIDATION-ERROR] Method argument validation failed                         ║");
      log.warn("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.warn("║ Correlation ID : {}", padRight(correlationId != null ? correlationId : "N/A", 63));
      log.warn("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));

      Map<String, String> errors = new HashMap<>();
      ex.getBindingResult().getFieldErrors().forEach(error -> {
      String fieldError = error.getField() + ": " + error.getDefaultMessage();
      errors.put(error.getField(), error.getDefaultMessage());
      log.warn("║ Field Error    : {}", padRight(fieldError, 63));
      });

      log.warn("║ Total Errors   : {}", padRight(String.valueOf(errors.size()), 63));
      log.warn("╚═══════════════════════════════════════════════════════════════════════════════╝");

      Map<String, Object> body = new LinkedHashMap<>();
      body.put("timestamp", LocalDateTime.now());
      body.put("error", "VALIDATION_FAILED");
      body.put("status", HttpStatus.BAD_REQUEST.value());
      body.put("correlationId", correlationId);
      body.put("details", errors);

      return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
      }

  /**
    * Handle custom validation exceptions
    * Returns 400 Bad Request
      */
      @ExceptionHandler(ValidationException.class)
      public ResponseEntity<?> handleValidationException(ValidationException ex) {
      String correlationId = MDC.get("correlationId");

      log.warn("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.warn("║ [VALIDATION-EXCEPTION] Custom validation failed                              ║");
      log.warn("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.warn("║ Correlation ID : {}", padRight(correlationId != null ? correlationId : "N/A", 63));
      log.warn("║ Error Message  : {}", padRight(ex.getMessage(), 63));
      log.warn("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));
      log.warn("╚═══════════════════════════════════════════════════════════════════════════════╝");

      Map<String, Object> body = new LinkedHashMap<>();
      body.put("timestamp", LocalDateTime.now());
      body.put("error", "VALIDATION_ERROR");
      body.put("status", HttpStatus.BAD_REQUEST.value());
      body.put("message", ex.getMessage());
      body.put("correlationId", correlationId);

      return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
      }

  /**
    * Handle image processing exceptions
    * Returns 500 Internal Server Error
      */
      @ExceptionHandler(ImageProcessingException.class)
      public ResponseEntity<?> handleImageProcessingException(ImageProcessingException ex) {
      String correlationId = MDC.get("correlationId");

      log.error("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.error("║ [IMAGE-PROCESSING-ERROR] Image processing failed                            ║");
      log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.error("║ Correlation ID : {}", padRight(correlationId != null ? correlationId : "N/A", 63));
      log.error("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));
      log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));

      if (ex.getCause() != null) {
      log.error("║ Root Cause     : {}", padRight(ex.getCause().getMessage(), 63));
      }

      log.error("║ Stack Trace:");
      log.error(ex.getMessage(), ex);
      log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");

      Map<String, Object> body = new LinkedHashMap<>();
      body.put("timestamp", LocalDateTime.now());
      body.put("error", "IMAGE_PROCESSING_FAILED");
      body.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
      body.put("message", ex.getMessage());
      body.put("correlationId", correlationId);

      return new ResponseEntity<>(body, HttpStatus.INTERNAL_SERVER_ERROR);
      }

  /**
    * Handle not found exceptions
    * Returns 404 Not Found
      */
      //    @ExceptionHandler(NotFoundException.class)
      //    public ResponseEntity<?> handleNotFoundException(NotFoundException ex) {
      //        String correlationId = MDC.get("correlationId");
      //
      //        log.warn("╔═══════════════════════════════════════════════════════════════════════════════╗");
      //        log.warn("║ [NOT-FOUND-ERROR] Resource not found                                         ║");
      //        log.warn("╠═══════════════════════════════════════════════════════════════════════════════╣");
      //        log.warn("║ Correlation ID : {}", padRight(correlationId != null ? correlationId : "N/A", 63));
      //        log.warn("║ Error Message  : {}", padRight(ex.getMessage(), 63));
      //        log.warn("╚═══════════════════════════════════════════════════════════════════════════════╝");
      //
      //        Map<String, Object> body = new LinkedHashMap<>();
      //        body.put("timestamp", LocalDateTime.now());
      //        body.put("error", "NOT_FOUND");
      //        body.put("status", HttpStatus.NOT_FOUND.value());
      //        body.put("message", ex.getMessage());
      //        body.put("correlationId", correlationId);
      //
      //        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
      //    }

  /**
    * Handle all unhandled exceptions
    * Returns 500 Internal Server Error
      */
      @ExceptionHandler(Exception.class)
      public ResponseEntity<?> handleGeneralException(Exception ex) {
      String correlationId = MDC.get("correlationId");
      if (correlationId == null) {
      correlationId = UUID.randomUUID().toString();
      }

      log.error("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.error("║ [UNHANDLED-EXCEPTION] An unexpected error occurred                          ║");
      log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.error("║ Correlation ID : {}", padRight(correlationId, 63));
      log.error("║ Error Type     : {}", padRight(ex.getClass().getName(), 63));
      log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));

      Throwable cause = ex.getCause();
      int depth = 0;
      while (cause != null && depth < 5) {
      log.error("║ [Cause {}] : {}", (depth + 1), cause.getClass().getSimpleName());
      log.error("║           Message: {}", cause.getMessage());
      cause = cause.getCause();
      depth++;
      }

      log.error("║ Stack Trace:");
      log.error(ex.getMessage(), ex);
      log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");

      Map<String, Object> body = new LinkedHashMap<>();
      body.put("timestamp", LocalDateTime.now());
      body.put("error", "INTERNAL_SERVER_ERROR");
      body.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
      body.put("message", "An unexpected error occurred. Reference ID: " + correlationId);
      body.put("correlationId", correlationId);

      return new ResponseEntity<>(body, HttpStatus.INTERNAL_SERVER_ERROR);
      }

  // ===== HELPER METHODS =====
  private String padRight(String s, int n) {
  if (s == null) s = "null";
  return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
  }
  }

========================================================================================================================
FILE PATH: Orbit_API/exception/ImageProcessingException.java
========================================================================================================================

package com.Orbit_API.exception;

/**
* Thrown when GDAL processing, MinIO upload, or GeoServer publish fails.
* Treated as a server-side error (500).
  */
  public class ImageProcessingException extends RuntimeException {

  public ImageProcessingException(String message) {
  super(message);
  }

  public ImageProcessingException(String message, Throwable cause) {
  super(message, cause);
  }
  }

========================================================================================================================
FILE PATH: Orbit_API/exception/NotFoundException.java
========================================================================================================================

package com.Orbit_API.exception;

/**
* Exception thrown when a requested resource is not found
* HTTP Status: 404 Not Found
  */
  public class NotFoundException extends RuntimeException {

  public NotFoundException(String message) {
  super(message);
  }

  public NotFoundException(String message, Throwable cause) {
  super(message, cause);
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/exception/ValidationException.java
========================================================================================================================

package com.Orbit_API.exception;

/**
* Thrown when user-supplied input fails business validation.
* Handled by GlobalExceptionHandler → 400 Bad Request.
  */
  public class ValidationException extends RuntimeException {

  public ValidationException(String message) {
  super(message);
  }

  public ValidationException(String message, Throwable cause) {
  super(message, cause);
  }
  }

========================================================================================================================
FILE PATH: Orbit_API/export/controller/RasterExportController.java
========================================================================================================================

package com.Orbit_API.export.controller;


import com.Orbit_API.export.dto.RasterExportRequestDTO;
import com.Orbit_API.export.dto.RasterExportResponseDTO;
import com.Orbit_API.export.dto.RasterExportStatusDTO;
import com.Orbit_API.export.exception.RasterExportException;
import com.Orbit_API.export.service.RasterExportService;
import com.Orbit_API.exception.NotFoundException;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

/**
* Export REST Controller — fully separate from SatelliteImageController.
*
* Endpoints:
*   POST  /api/v1/exports/images/{id}          Submit export job
*   GET   /api/v1/exports/{exportId}/status     Poll job status
*   GET   /api/v1/exports/{exportId}/download   Get signed ZIP download URL
*   GET   /api/v1/exports/{exportId}            Full job detail
    */
    @Slf4j
    @RestController
    @RequestMapping("/api/v1/exports")
    public class RasterExportController {

private final RasterExportService exportService;

public RasterExportController(RasterExportService exportService) {
this.exportService = exportService;
}

/**
* POST /api/v1/exports/images/{id}
* Submit a new export job for the given satellite image.
* Returns 202 Accepted immediately — poll /status to track progress.
  */
  @PostMapping("/images/{id}")
  public ResponseEntity<RasterExportResponseDTO> submitExport(
  @PathVariable UUID id,
  @Valid @RequestBody RasterExportRequestDTO request,
  @RequestHeader(value = "X-User-Id", defaultValue = "anonymous") String userId) {

  long start = System.currentTimeMillis();
  log.info("[EXPORT-REQUEST] imageId={} format={} type={} tileSize={} user={}",
  id, request.getFormat(), request.getExportType(), request.getTileSize(), userId);
  try {
  RasterExportResponseDTO response = exportService.submitExport(id, request, userId);
  log.info("[EXPORT-ACCEPTED] exportId={} in {}ms", response.getExportId(),
  System.currentTimeMillis() - start);
  return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);  // 202
  } catch (NotFoundException ex) {
  log.warn("[EXPORT-NOT-FOUND] imageId={}: {}", id, ex.getMessage());
  return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
  } catch (RasterExportException ex) {
  log.warn("[EXPORT-REJECTED] imageId={}: {}", id, ex.getMessage());
  return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
  } catch (Exception ex) {
  log.error("[EXPORT-ERROR] imageId={}: {}", id, ex.getMessage(), ex);
  return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
  }
  }

/**
* GET /api/v1/exports/{exportId}/status
* Poll export job progress. Frontend calls every 3–5 seconds.
  */
  @GetMapping("/{exportId}/status")
  public ResponseEntity<RasterExportStatusDTO> getStatus(@PathVariable UUID exportId) {
  log.debug("[EXPORT-STATUS-POLL] exportId={}", exportId);
  try {
  RasterExportStatusDTO status = exportService.getStatus(exportId);
  return ResponseEntity.ok(status);
  } catch (NotFoundException ex) {
  return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
  }
  }

/**
* GET /api/v1/exports/{exportId}/download
* Returns a fresh 60-minute signed MinIO URL for the ZIP.
* Only works when status == COMPLETED.
  */
  @GetMapping("/{exportId}/download")
  public ResponseEntity<String> download(@PathVariable UUID exportId) {
  log.info("[EXPORT-DOWNLOAD-URL] exportId={}", exportId);
  try {
  String url = exportService.getDownloadUrl(exportId);
  return ResponseEntity.ok(url);
  } catch (NotFoundException ex) {
  return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
  } catch (RasterExportException ex) {
  log.warn("[EXPORT-DOWNLOAD-NOT-READY] exportId={}: {}", exportId, ex.getMessage());
  return ResponseEntity.status(HttpStatus.CONFLICT).build();  // 409 — not ready yet
  }
  }

/**
* GET /api/v1/exports/{exportId}
* Full job detail — same as status but always available.
  */
  @GetMapping("/{exportId}")
  public ResponseEntity<RasterExportStatusDTO> getExport(@PathVariable UUID exportId) {
  try {
  return ResponseEntity.ok(exportService.getStatus(exportId));
  } catch (NotFoundException ex) {
  return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
  }
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/dto/RasterExportRequestDTO.java
========================================================================================================================

package com.Orbit_API.export.dto;



import com.Orbit_API.export.entity.ExportFormat;
import com.Orbit_API.export.entity.ExportType;
import jakarta.validation.constraints.*;

/**
* Request body for POST /api/v1/exports/images/{id}
  */
  public class RasterExportRequestDTO {

  /** Optional GeoJSON polygon string for AOI clipping. Null = use full COG extent. */
  private String aoiGeoJson;

  @NotNull(message = "Export format is required (PNG or JPEG)")
  private ExportFormat format;

  @NotNull(message = "Export type is required (TILED, CLIPPED, or BOTH)")
  private ExportType exportType;

  /**
    * Pixel tile size for TILED / BOTH modes.
    * Ignored for CLIPPED. Defaults to 1024 if null.
      */
      @Min(value = 64,   message = "Tile size must be at least 64 pixels")
      @Max(value = 4096, message = "Tile size must not exceed 4096 pixels")
      private Integer tileSize = 1024;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public String getAoiGeoJson()                       { return aoiGeoJson; }
  public void setAoiGeoJson(String aoiGeoJson)        { this.aoiGeoJson = aoiGeoJson; }
  public ExportFormat getFormat()                     { return format; }
  public void setFormat(ExportFormat format)          { this.format = format; }
  public ExportType getExportType()                   { return exportType; }
  public void setExportType(ExportType exportType)    { this.exportType = exportType; }
  public Integer getTileSize()                        { return tileSize; }
  public void setTileSize(Integer tileSize)           { this.tileSize = tileSize; }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/dto/RasterExportResponseDTO.java
========================================================================================================================

package com.Orbit_API.export.dto;



import com.Orbit_API.export.entity.ExportFormat;
import com.Orbit_API.export.entity.ExportStatus;
import com.Orbit_API.export.entity.ExportType;

import java.time.LocalDateTime;
import java.util.UUID;

/**
* Returned immediately (202 Accepted) after submitting an export job.
  */
  public class RasterExportResponseDTO {

  private UUID exportId;
  private UUID imageId;
  private String imageCode;
  private ExportStatus status;
  private ExportFormat format;
  private ExportType exportType;
  private Integer tileSize;
  private String statusUrl;       // GET /api/v1/exports/{exportId}/status
  private String downloadUrl;     // null until COMPLETED
  private LocalDateTime createdAt;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public UUID getExportId()                       { return exportId; }
  public void setExportId(UUID id)                { this.exportId = id; }
  public UUID getImageId()                        { return imageId; }
  public void setImageId(UUID id)                 { this.imageId = id; }
  public String getImageCode()                    { return imageCode; }
  public void setImageCode(String c)              { this.imageCode = c; }
  public ExportStatus getStatus()                 { return status; }
  public void setStatus(ExportStatus s)           { this.status = s; }
  public ExportFormat getFormat()                 { return format; }
  public void setFormat(ExportFormat f)           { this.format = f; }
  public ExportType getExportType()               { return exportType; }
  public void setExportType(ExportType t)         { this.exportType = t; }
  public Integer getTileSize()                    { return tileSize; }
  public void setTileSize(Integer s)              { this.tileSize = s; }
  public String getStatusUrl()                    { return statusUrl; }
  public void setStatusUrl(String u)              { this.statusUrl = u; }
  public String getDownloadUrl()                  { return downloadUrl; }
  public void setDownloadUrl(String u)            { this.downloadUrl = u; }
  public LocalDateTime getCreatedAt()             { return createdAt; }
  public void setCreatedAt(LocalDateTime t)       { this.createdAt = t; }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/dto/RasterExportStatusDTO.java
========================================================================================================================

package com.Orbit_API.export.dto;



import com.Orbit_API.export.entity.ExportFormat;
import com.Orbit_API.export.entity.ExportStatus;
import com.Orbit_API.export.entity.ExportType;

import java.time.LocalDateTime;
import java.util.UUID;

/**
* Returned by GET /api/v1/exports/{exportId}/status — polled by frontend.
  */
  public class RasterExportStatusDTO {

  private UUID exportId;
  private UUID imageId;
  private ExportStatus status;
  private ExportFormat format;
  private ExportType exportType;
  private Integer tileSize;
  private Integer outputCount;        // how many patches were generated
  private int progress;               // 0–100
  private String currentStep;         // human-readable step description
  private String downloadUrl;         // non-null only when COMPLETED
  private String errorMessage;        // non-null only when FAILED
  private LocalDateTime createdAt;
  private LocalDateTime updatedAt;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public UUID getExportId()                       { return exportId; }
  public void setExportId(UUID id)                { this.exportId = id; }
  public UUID getImageId()                        { return imageId; }
  public void setImageId(UUID id)                 { this.imageId = id; }
  public ExportStatus getStatus()                 { return status; }
  public void setStatus(ExportStatus s)           { this.status = s; }
  public ExportFormat getFormat()                 { return format; }
  public void setFormat(ExportFormat f)           { this.format = f; }
  public ExportType getExportType()               { return exportType; }
  public void setExportType(ExportType t)         { this.exportType = t; }
  public Integer getTileSize()                    { return tileSize; }
  public void setTileSize(Integer s)              { this.tileSize = s; }
  public Integer getOutputCount()                 { return outputCount; }
  public void setOutputCount(Integer n)           { this.outputCount = n; }
  public int getProgress()                        { return progress; }
  public void setProgress(int p)                  { this.progress = p; }
  public String getCurrentStep()                  { return currentStep; }
  public void setCurrentStep(String s)            { this.currentStep = s; }
  public String getDownloadUrl()                  { return downloadUrl; }
  public void setDownloadUrl(String u)            { this.downloadUrl = u; }
  public String getErrorMessage()                 { return errorMessage; }
  public void setErrorMessage(String m)           { this.errorMessage = m; }
  public LocalDateTime getCreatedAt()             { return createdAt; }
  public void setCreatedAt(LocalDateTime t)       { this.createdAt = t; }
  public LocalDateTime getUpdatedAt()             { return updatedAt; }
  public void setUpdatedAt(LocalDateTime t)       { this.updatedAt = t; }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/entity/ExportFormat.java
========================================================================================================================

package com.Orbit_API.export.entity;

public enum ExportFormat {
PNG,
JPEG
}

========================================================================================================================
FILE PATH: Orbit_API/export/entity/ExportStatus.java
========================================================================================================================

package com.Orbit_API.export.entity;


public enum ExportStatus {
PENDING,        // Job created, waiting for async thread
PROCESSING,     // GDAL operations running
ZIPPING,        // Patching complete, creating ZIP
UPLOADING,      // ZIP uploading to MinIO
COMPLETED,      // ZIP in MinIO, download URL ready
FAILED          // Terminal failure — check errorMessage
}


========================================================================================================================
FILE PATH: Orbit_API/export/entity/ExportType.java
========================================================================================================================

package com.Orbit_API.export.entity;

public enum ExportType {
TILED,      // Split full COG into fixed-size patches
CLIPPED,    // Clip to AOI polygon only, single output
BOTH        // Clip to AOI first, then tile the clipped result
}


========================================================================================================================
FILE PATH: Orbit_API/export/entity/RasterExportJob.java
========================================================================================================================

package com.Orbit_API.export.entity;


import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
* Persistent record of one export job.
* Stored in: raster_export_jobs
* Lifecycle: PENDING → PROCESSING → ZIPPING → UPLOADING → COMPLETED (or FAILED)
  */
  @Entity
  @Table(name = "raster_export_jobs", indexes = {
  @Index(name = "idx_export_jobs_image_id",   columnList = "image_id"),
  @Index(name = "idx_export_jobs_status",     columnList = "status"),
  @Index(name = "idx_export_jobs_created_at", columnList = "created_at")
  })
  public class RasterExportJob {

  @Id
  @GeneratedValue
  private UUID exportId;

  @Column(name = "image_id", nullable = false)
  private UUID imageId;

  @Column(name = "image_code")
  private String imageCode;

  @Enumerated(EnumType.STRING)
  @Column(name = "export_format", nullable = false)
  private ExportFormat exportFormat;

  @Enumerated(EnumType.STRING)
  @Column(name = "export_type", nullable = false)
  private ExportType exportType;

  @Column(name = "tile_size")
  private Integer tileSize;                   // pixel width/height per patch, e.g. 1024

  @Column(name = "aoi_geo_json", columnDefinition = "TEXT")
  private String aoiGeoJson;                  // null if no AOI clipping requested

  @Enumerated(EnumType.STRING)
  @Column(name = "status", nullable = false)
  private ExportStatus status;

  @Column(name = "output_count")
  private Integer outputCount;                // number of patches generated

  @Column(name = "minio_zip_path")
  private String minioZipPath;                // e.g. exports/IMG-xxx/export-<id>.zip

  @Column(name = "error_message", columnDefinition = "TEXT")
  private String errorMessage;

  @Column(name = "requested_by")
  private String requestedBy;                 // userId / "system"

  @Column(name = "created_at", nullable = false)
  private LocalDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private LocalDateTime updatedAt;

  @PrePersist
  public void onCreate() {
  this.createdAt = LocalDateTime.now();
  this.updatedAt = LocalDateTime.now();
  if (this.status == null) this.status = ExportStatus.PENDING;
  }

  @PreUpdate
  public void onUpdate() {
  this.updatedAt = LocalDateTime.now();
  }

  // ── Getters & Setters ───────────────────────────────────────────────────
  public UUID getExportId()                       { return exportId; }
  public void setExportId(UUID exportId)          { this.exportId = exportId; }
  public UUID getImageId()                        { return imageId; }
  public void setImageId(UUID imageId)            { this.imageId = imageId; }
  public String getImageCode()                    { return imageCode; }
  public void setImageCode(String imageCode)      { this.imageCode = imageCode; }
  public ExportFormat getExportFormat()           { return exportFormat; }
  public void setExportFormat(ExportFormat f)     { this.exportFormat = f; }
  public ExportType getExportType()               { return exportType; }
  public void setExportType(ExportType t)         { this.exportType = t; }
  public Integer getTileSize()                    { return tileSize; }
  public void setTileSize(Integer tileSize)       { this.tileSize = tileSize; }
  public String getAoiGeoJson()                   { return aoiGeoJson; }
  public void setAoiGeoJson(String aoiGeoJson)    { this.aoiGeoJson = aoiGeoJson; }
  public ExportStatus getStatus()                 { return status; }
  public void setStatus(ExportStatus status)      { this.status = status; }
  public Integer getOutputCount()                 { return outputCount; }
  public void setOutputCount(Integer n)           { this.outputCount = n; }
  public String getMinioZipPath()                 { return minioZipPath; }
  public void setMinioZipPath(String path)        { this.minioZipPath = path; }
  public String getErrorMessage()                 { return errorMessage; }
  public void setErrorMessage(String msg)         { this.errorMessage = msg; }
  public String getRequestedBy()                  { return requestedBy; }
  public void setRequestedBy(String user)         { this.requestedBy = user; }
  public LocalDateTime getCreatedAt()             { return createdAt; }
  public LocalDateTime getUpdatedAt()             { return updatedAt; }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/exception/RasterExportException.java
========================================================================================================================

package com.Orbit_API.export.exception;

public class RasterExportException extends RuntimeException {

    public RasterExportException(String message) {
        super(message);
    }

    public RasterExportException(String message, Throwable cause) {
        super(message, cause);
    }
}


========================================================================================================================
FILE PATH: Orbit_API/export/mapper/RasterExportMapper.java
========================================================================================================================

package com.Orbit_API.export.mapper;


import com.Orbit_API.export.dto.RasterExportResponseDTO;
import com.Orbit_API.export.dto.RasterExportStatusDTO;
import com.Orbit_API.export.entity.ExportStatus;
import com.Orbit_API.export.entity.RasterExportJob;
import org.springframework.stereotype.Component;

/**
* Converts RasterExportJob entity → response DTOs.
* No business logic — pure mapping only.
  */
  @Component
  public class RasterExportMapper {

  public RasterExportResponseDTO toResponse(RasterExportJob job) {
  RasterExportResponseDTO dto = new RasterExportResponseDTO();
  dto.setExportId(job.getExportId());
  dto.setImageId(job.getImageId());
  dto.setImageCode(job.getImageCode());
  dto.setStatus(job.getStatus());
  dto.setFormat(job.getExportFormat());
  dto.setExportType(job.getExportType());
  dto.setTileSize(job.getTileSize());
  dto.setStatusUrl("/api/v1/exports/" + job.getExportId() + "/status");
  dto.setDownloadUrl(null);   // always null at creation time
  dto.setCreatedAt(job.getCreatedAt());
  return dto;
  }

  public RasterExportStatusDTO toStatus(RasterExportJob job, String downloadUrl) {
  RasterExportStatusDTO dto = new RasterExportStatusDTO();
  dto.setExportId(job.getExportId());
  dto.setImageId(job.getImageId());
  dto.setStatus(job.getStatus());
  dto.setFormat(job.getExportFormat());
  dto.setExportType(job.getExportType());
  dto.setTileSize(job.getTileSize());
  dto.setOutputCount(job.getOutputCount());
  dto.setProgress(resolveProgress(job.getStatus()));
  dto.setCurrentStep(resolveStep(job.getStatus()));
  dto.setDownloadUrl(job.getStatus() == ExportStatus.COMPLETED ? downloadUrl : null);
  dto.setErrorMessage(job.getStatus() == ExportStatus.FAILED ? job.getErrorMessage() : null);
  dto.setCreatedAt(job.getCreatedAt());
  dto.setUpdatedAt(job.getUpdatedAt());
  return dto;
  }

  private int resolveProgress(ExportStatus status) {
  return switch (status) {
  case PENDING    -> 0;
  case PROCESSING -> 40;
  case ZIPPING    -> 75;
  case UPLOADING  -> 90;
  case COMPLETED  -> 100;
  case FAILED     -> -1;
  };
  }

  private String resolveStep(ExportStatus status) {
  return switch (status) {
  case PENDING    -> "Queued for export";
  case PROCESSING -> "Generating image patches via GDAL";
  case ZIPPING    -> "Zipping output patches";
  case UPLOADING  -> "Uploading ZIP to MinIO";
  case COMPLETED  -> "Export complete — ready for download";
  case FAILED     -> "Export failed — see errorMessage";
  };
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/processing/GdalRasterExportService.java
========================================================================================================================

package com.Orbit_API.export.processing;



import com.Orbit_API.export.entity.ExportFormat;
import com.Orbit_API.export.exception.RasterExportException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/**
* All GDAL shell operations for the export pipeline.
* Responsibilities:
*   1. clipToAoi()     — gdalwarp with -cutline for AOI polygon clipping
*   2. tileRaster()    — gdal_translate loop to produce fixed-size patches
*   3. zipDirectory()  — zip all patches into one archive
*
* This class never touches MinIO or the DB — pure raster/filesystem operations.
  */
  @Slf4j
  @Service
  public class GdalRasterExportService {

  @Value("${gdal.path}")
  private String gdalPath;

  @Value("${gdal.python.path:gdal_retile.py}")
  private String gdalRetilePath;

  /**
    * Clips a COG to the AOI polygon using gdalwarp -cutline.
    *
    * GDAL command produced:
    *   gdalwarp -cutline /tmp/aoi.geojson -crop_to_cutline
    *            -of GTiff input.tif clipped.tif
    *
    * @param inputCog    local path to COG file
    * @param aoiGeoJson  GeoJSON polygon string
    * @param outputDir   working directory
    * @param correlationId for logging
    * @return path to clipped GeoTIFF
      */
      public Path clipToAoi(Path inputCog, String aoiGeoJson, Path outputDir, String correlationId) {
      log.info("[EXPORT-CLIP-START] correlationId={} input={}", correlationId, inputCog);
      try {
      // Write AOI to a temp GeoJSON file — gdalwarp needs a file, not a string
      Path aoiFile = outputDir.resolve("aoi_cutline.geojson");
      Files.writeString(aoiFile, aoiGeoJson);

           Path clippedOutput = outputDir.resolve("clipped.tif");

           List<String> cmd = List.of(
                   gdalPath + "/gdalwarp",
                   "-cutline",    aoiFile.toAbsolutePath().toString(),
                   "-crop_to_cutline",
                   "-of",         "GTiff",
                   "-co",         "COMPRESS=LZW",
                   "-overwrite",
                   inputCog.toAbsolutePath().toString(),
                   clippedOutput.toAbsolutePath().toString()
           );

           runCommand(cmd, "GDAL-CLIP", correlationId);
           log.info("[EXPORT-CLIP-SUCCESS] correlationId={} output={}", correlationId, clippedOutput);
           return clippedOutput;

      } catch (Exception ex) {
      throw new RasterExportException("AOI clipping failed: " + ex.getMessage(), ex);
      }
      }

  /**
    * Splits a raster into fixed-size PNG or JPEG patches using gdal_translate.
    *
    * Strategy: read raster dimensions via gdalinfo, then iterate over a grid
    * of (tileSize x tileSize) windows and extract each with gdal_translate -srcwin.
    *
    * GDAL command per patch:
    *   gdal_translate -of PNG -srcwin xOff yOff tileW tileH input.tif tile_row_col.png
    *
    * @param inputRaster source raster (full COG or already-clipped TIF)
    * @param outputDir   directory to write patches into
    * @param tileSize    pixel width and height of each patch
    * @param format      PNG or JPEG
    * @param correlationId for logging
    * @return list of generated patch file paths
      */
      public List<Path> tileRaster(Path inputRaster, Path outputDir,
      int tileSize, ExportFormat format,
      String correlationId) {
      log.info("[EXPORT-TILE-START] correlationId={} tileSize={}px format={} input={}",
      correlationId, tileSize, format, inputRaster);
      try {
      // Read raster dimensions (width, height) from gdalinfo JSON output
      int[] dims = readRasterDimensions(inputRaster, correlationId);
      int rasterWidth  = dims[0];
      int rasterHeight = dims[1];

           String ext       = format == ExportFormat.PNG ? ".png" : ".jpg";
           String gdalOf    = format == ExportFormat.PNG ? "PNG"  : "JPEG";

           List<Path> patches = new ArrayList<>();
           int tileRow = 0;

           for (int yOff = 0; yOff < rasterHeight; yOff += tileSize, tileRow++) {
               int tileCol = 0;
               int tileH   = Math.min(tileSize, rasterHeight - yOff);

               for (int xOff = 0; xOff < rasterWidth; xOff += tileSize, tileCol++) {
                   int tileW = Math.min(tileSize, rasterWidth - xOff);

                   String patchName = String.format("patch_%04d_%04d%s", tileRow, tileCol, ext);
                   Path patchFile   = outputDir.resolve(patchName);

                   List<String> cmd = new ArrayList<>(List.of(
                           gdalPath + "/gdal_translate",
                           "-of",      gdalOf,
                           "-srcwin",
                           String.valueOf(xOff),
                           String.valueOf(yOff),
                           String.valueOf(tileW),
                           String.valueOf(tileH),
                           inputRaster.toAbsolutePath().toString(),
                           patchFile.toAbsolutePath().toString()
                   ));

                   // JPEG quality
                   if (format == ExportFormat.JPEG) {
                       cmd.add(3, "-co"); cmd.add(4, "QUALITY=90");
                   }

                   runCommand(cmd, "GDAL-TILE-" + tileRow + "-" + tileCol, correlationId);
                   patches.add(patchFile);
                   log.debug("[EXPORT-TILE-PATCH] {} created", patchName);
               }
           }

           log.info("[EXPORT-TILE-SUCCESS] correlationId={} totalPatches={}", correlationId, patches.size());
           return patches;

      } catch (RasterExportException rex) {
      throw rex;
      } catch (Exception ex) {
      throw new RasterExportException("Raster tiling failed: " + ex.getMessage(), ex);
      }
      }

  /**
    * Zips all files in patchDir into a single ZIP archive.
    *
    * @param patchDir     directory containing patch files
    * @param zipOutputPath full path for the resulting ZIP file
    * @param correlationId for logging
    * @return path to the created ZIP
      */
      public Path zipDirectory(Path patchDir, Path zipOutputPath, String correlationId) {
      log.info("[EXPORT-ZIP-START] correlationId={} source={}", correlationId, patchDir);
      try (var zipOut = new java.util.zip.ZipOutputStream(
      new BufferedOutputStream(new FileOutputStream(zipOutputPath.toFile())))) {

           try (Stream<Path> files = Files.walk(patchDir)) {
               files.filter(Files::isRegularFile).forEach(file -> {
                   try {
                       String entryName = patchDir.relativize(file).toString();
                       zipOut.putNextEntry(new java.util.zip.ZipEntry(entryName));
                       Files.copy(file, zipOut);
                       zipOut.closeEntry();
                       log.debug("[EXPORT-ZIP-ENTRY] Added: {}", entryName);
                   } catch (IOException e) {
                       throw new UncheckedIOException(e);
                   }
               });
           }

           log.info("[EXPORT-ZIP-SUCCESS] correlationId={} zipFile={}", correlationId, zipOutputPath);
           return zipOutputPath;

      } catch (Exception ex) {
      throw new RasterExportException("ZIP creation failed: " + ex.getMessage(), ex);
      }
      }

  // ── Private Helpers ─────────────────────────────────────────────────────

  /**
    * Reads raster pixel dimensions using gdalinfo -json.
    * Parses the "size" array: [width, height].
      */
      private int[] readRasterDimensions(Path raster, String correlationId) throws Exception {
      List<String> cmd = List.of(
      gdalPath + "/gdalinfo", "-json", raster.toAbsolutePath().toString()
      );
      String output = runCommandGetOutput(cmd, "GDAL-INFO-DIMS", correlationId);

      com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
      com.fasterxml.jackson.databind.JsonNode root = mapper.readTree(output);
      com.fasterxml.jackson.databind.JsonNode sizeNode = root.path("size");

      if (sizeNode.isMissingNode() || !sizeNode.isArray() || sizeNode.size() < 2) {
      throw new RasterExportException("Could not read raster dimensions from gdalinfo output");
      }
      int width  = sizeNode.get(0).asInt();
      int height = sizeNode.get(1).asInt();
      log.debug("[GDAL-DIMS] correlationId={} width={} height={}", correlationId, width, height);
      return new int[]{width, height};
      }

  /** Runs a command and asserts exit code == 0. Throws RasterExportException on failure. */
  private void runCommand(List<String> cmd, String label, String correlationId) {
  try {
  log.debug("[{}] correlationId={} cmd={}", label, correlationId, String.join(" ", cmd));
  ProcessBuilder pb = new ProcessBuilder(cmd);
  pb.redirectErrorStream(true);
  Process process   = pb.start();

           StringBuilder output = new StringBuilder();
           try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
               String line;
               while ((line = reader.readLine()) != null) output.append(line).append("\n");
           }

           int exitCode = process.waitFor();
           if (exitCode != 0) {
               log.error("[{}-FAILED] correlationId={} exitCode={} output={}",
                       label, correlationId, exitCode, output);
               throw new RasterExportException(label + " failed. Exit code: " + exitCode);
           }
       } catch (RasterExportException rex) {
           throw rex;
       } catch (Exception ex) {
           throw new RasterExportException(label + " process error: " + ex.getMessage(), ex);
       }
  }

  /** Runs a command and returns stdout as a String. */
  private String runCommandGetOutput(List<String> cmd, String label, String correlationId) {
  try {
  ProcessBuilder pb = new ProcessBuilder(cmd);
  pb.redirectErrorStream(true);
  Process process   = pb.start();

           StringBuilder output = new StringBuilder();
           try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
               String line;
               while ((line = reader.readLine()) != null) output.append(line).append("\n");
           }

           int exitCode = process.waitFor();
           if (exitCode != 0) {
               throw new RasterExportException(label + " failed. Exit: " + exitCode);
           }
           return output.toString();
       } catch (RasterExportException rex) {
           throw rex;
       } catch (Exception ex) {
           throw new RasterExportException(label + " process error: " + ex.getMessage(), ex);
       }
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/export/repository/RasterExportJobRepository.java
========================================================================================================================

package com.Orbit_API.export.repository;



import com.Orbit_API.export.entity.ExportStatus;
import com.Orbit_API.export.entity.RasterExportJob;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface RasterExportJobRepository extends JpaRepository<RasterExportJob, UUID> {

    List<RasterExportJob> findByImageIdOrderByCreatedAtDesc(UUID imageId);

    List<RasterExportJob> findByStatusOrderByCreatedAtAsc(ExportStatus status);

    List<RasterExportJob> findByRequestedByOrderByCreatedAtDesc(String requestedBy);
}


========================================================================================================================
FILE PATH: Orbit_API/export/service/RasterExportService.java
========================================================================================================================

package com.Orbit_API.export.service;



import com.Orbit_API.export.dto.RasterExportRequestDTO;
import com.Orbit_API.export.dto.RasterExportResponseDTO;
import com.Orbit_API.export.dto.RasterExportStatusDTO;

import java.util.UUID;

public interface RasterExportService {

    /**
     * Creates export job record (PENDING) and queues async processing.
     * Returns 202 immediately.
     */
    RasterExportResponseDTO submitExport(UUID imageId, RasterExportRequestDTO request, String userId);

    /**
     * Returns current status and download URL (if COMPLETED).
     */
    RasterExportStatusDTO getStatus(UUID exportId);

    /**
     * Returns a fresh signed MinIO download URL for a COMPLETED export.
     */
    String getDownloadUrl(UUID exportId);
}


========================================================================================================================
FILE PATH: Orbit_API/export/service/impl/RasterExportServiceImpl.java
========================================================================================================================

package com.Orbit_API.export.service.impl;



import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.export.dto.RasterExportRequestDTO;
import com.Orbit_API.export.dto.RasterExportResponseDTO;
import com.Orbit_API.export.dto.RasterExportStatusDTO;
import com.Orbit_API.export.entity.ExportStatus;
import com.Orbit_API.export.entity.ExportType;
import com.Orbit_API.export.entity.RasterExportJob;
import com.Orbit_API.export.exception.RasterExportException;
import com.Orbit_API.export.mapper.RasterExportMapper;
import com.Orbit_API.export.processing.GdalRasterExportService;
import com.Orbit_API.export.repository.RasterExportJobRepository;
import com.Orbit_API.export.service.RasterExportService;
import com.Orbit_API.exception.NotFoundException;
import com.Orbit_API.storage.MinioStorageService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.InputStream;
import java.nio.file.*;
import java.util.List;
import java.util.UUID;

@Slf4j
@Service
public class RasterExportServiceImpl implements RasterExportService {

    private final SatelliteImageRepository   imageRepository;
    private final RasterExportJobRepository  exportRepository;
    private final GdalRasterExportService    gdalExportService;
    private final MinioStorageService        minioStorageService;
    private final RasterExportMapper         mapper;

    @Value("${minio.bucket-cog}")
    private String cogBucket;

    @Value("${minio.bucket-exports:orbitview-exports}")
    private String exportBucket;

    @Value("${app.upload.temp-dir:/tmp/orbitview}")
    private String tempDir;

    public RasterExportServiceImpl(SatelliteImageRepository imageRepository,
                                   RasterExportJobRepository exportRepository,
                                   GdalRasterExportService gdalExportService,
                                   MinioStorageService minioStorageService,
                                   RasterExportMapper mapper) {
        this.imageRepository  = imageRepository;
        this.exportRepository = exportRepository;
        this.gdalExportService = gdalExportService;
        this.minioStorageService = minioStorageService;
        this.mapper = mapper;
    }

    // ── A. SUBMIT ──────────────────────────────────────────────────────────

    @Override
    @Transactional
    public RasterExportResponseDTO submitExport(UUID imageId,
                                                RasterExportRequestDTO request,
                                                String userId) {
        log.info("[EXPORT-SUBMIT] imageId={} format={} type={} tileSize={} user={}",
                imageId, request.getFormat(), request.getExportType(),
                request.getTileSize(), userId);

        // Validate image exists and has a COG
        SatelliteImage image = imageRepository.findById(imageId)
                .orElseThrow(() -> new NotFoundException("Image not found: " + imageId));

        if (image.getCogObjectPath() == null) {
            throw new RasterExportException(
                    "Image " + imageId + " has no COG path — processing may not be complete yet");
        }

        // Create and persist PENDING job
        RasterExportJob job = new RasterExportJob();
        job.setImageId(imageId);
        job.setImageCode(image.getImageCode());
        job.setExportFormat(request.getFormat());
        job.setExportType(request.getExportType());
        job.setTileSize(request.getTileSize() != null ? request.getTileSize() : 1024);
        job.setAoiGeoJson(request.getAoiGeoJson());
        job.setRequestedBy(userId != null ? userId : "anonymous");
        job.setStatus(ExportStatus.PENDING);
        RasterExportJob savedJob = exportRepository.save(job);

        log.info("[EXPORT-SUBMIT-ACCEPTED] exportId={} imageCode={}",
                savedJob.getExportId(), savedJob.getImageCode());

        // Trigger async processing — returns immediately
        runExportAsync(savedJob.getExportId(), image.getCogObjectPath());

        return mapper.toResponse(savedJob);
    }

    // ── B. ASYNC BACKGROUND PROCESSING ────────────────────────────────────

    @Async("imageProcessingExecutor")
    public void runExportAsync(UUID exportId, String cogObjectPath) {
        String correlationId = UUID.randomUUID().toString();
        log.info("[EXPORT-PIPELINE-START] exportId={} correlationId={}", exportId, correlationId);

        Path workDir     = null;
        Path localCog    = null;

        try {
            RasterExportJob job = exportRepository.findById(exportId)
                    .orElseThrow(() -> new RasterExportException("Export job not found: " + exportId));

            // Mark PROCESSING
            job.setStatus(ExportStatus.PROCESSING);
            exportRepository.save(job);

            // STEP 1 — Download COG from MinIO to local temp
            workDir  = Files.createDirectories(
                    Path.of(tempDir, "exports", exportId.toString()));
            localCog = workDir.resolve("source.tif");


            log.info("[EXPORT-STEP-1] Downloading COG from MinIO: bucket={} path={}",
                    cogBucket, cogObjectPath);

            downloadCogFromMinio(cogBucket, cogObjectPath, localCog);

            log.info("[EXPORT-STEP-1-OK] COG downloaded to {}", localCog);


//            log.info("[EXPORT-STEP-1] Downloading COG from MinIO: bucket={} path={}",
//                    cogBucket, cogObjectPath);
//            try (InputStream cogStream = minioStorageService
//                    .createSignedDownloadUrl(cogBucket, cogObjectPath, 60)
//                    .describeConstable().map(u -> {
//                        throw new UnsupportedOperationException("use direct download");
//                    }).orElseThrow()) {
//                // Use uploadFile approach — download directly via MinIO client
//            } catch (UnsupportedOperationException ignored) {
//                // Intentional: download the COG bytes via MinioClient directly
//                downloadCogFromMinio(cogBucket, cogObjectPath, localCog);
//            }
//            log.info("[EXPORT-STEP-1-OK] COG downloaded to {}", localCog);

            // STEP 2 — Optional AOI clipping
            Path rasterForTiling = localCog;
            if (job.getAoiGeoJson() != null
                    && (job.getExportType() == ExportType.CLIPPED
                    || job.getExportType() == ExportType.BOTH)) {
                log.info("[EXPORT-STEP-2] Clipping to AOI polygon");
                rasterForTiling = gdalExportService.clipToAoi(
                        localCog, job.getAoiGeoJson(), workDir, correlationId);
                log.info("[EXPORT-STEP-2-OK] Clipped raster: {}", rasterForTiling);
            } else {
                log.info("[EXPORT-STEP-2-SKIP] No AOI or TILED-only mode — skipping clip");
            }

            // STEP 3 — Tiling (skip for CLIPPED-only)
            Path patchDir = Files.createDirectories(workDir.resolve("patches"));
            List<Path> patches;

            if (job.getExportType() == ExportType.CLIPPED) {
                // No tiling — just copy the clipped file as the single output
                Path singleOutput = patchDir.resolve(
                        "clipped_output." + job.getExportFormat().name().toLowerCase());
                Files.copy(rasterForTiling, singleOutput,
                        StandardCopyOption.REPLACE_EXISTING);
                patches = List.of(singleOutput);
                log.info("[EXPORT-STEP-3-CLIPPED] Single clipped output: {}", singleOutput);
            } else {
                log.info("[EXPORT-STEP-3] Tiling raster into {}px patches", job.getTileSize());
                patches = gdalExportService.tileRaster(
                        rasterForTiling, patchDir,
                        job.getTileSize(), job.getExportFormat(),
                        correlationId);
                log.info("[EXPORT-STEP-3-OK] {} patches created", patches.size());
            }

            job.setOutputCount(patches.size());

            // STEP 4 — ZIP
            job.setStatus(ExportStatus.ZIPPING);
            exportRepository.save(job);
            log.info("[EXPORT-STEP-4] Zipping {} patches", patches.size());

            Path zipFile = workDir.resolve(
                    "export-" + exportId + "." + job.getExportFormat().name().toLowerCase() + ".zip");
            gdalExportService.zipDirectory(patchDir, zipFile, correlationId);
            log.info("[EXPORT-STEP-4-OK] ZIP created: {}", zipFile);

            // STEP 5 — Upload ZIP to MinIO
            job.setStatus(ExportStatus.UPLOADING);
            exportRepository.save(job);

            String zipObjectPath = "exports/" + job.getImageCode() + "/export-" + exportId + ".zip";
            log.info("[EXPORT-STEP-5] Uploading ZIP to MinIO bucket={} path={}", exportBucket, zipObjectPath);
            minioStorageService.uploadFile(exportBucket, zipObjectPath, zipFile);
            log.info("[EXPORT-STEP-5-OK] ZIP uploaded to MinIO");

            // STEP 6 — Mark COMPLETED
            job.setMinioZipPath(zipObjectPath);
            job.setStatus(ExportStatus.COMPLETED);
            exportRepository.save(job);

            log.info("[EXPORT-PIPELINE-SUCCESS] exportId={} patches={} correlationId={}",
                    exportId, patches.size(), correlationId);

        } catch (Exception ex) {
            log.error("[EXPORT-PIPELINE-FAILED] exportId={} correlationId={} error={}",
                    exportId, correlationId, ex.getMessage(), ex);
            try {
                RasterExportJob job = exportRepository.findById(exportId).orElse(null);
                if (job != null) {
                    job.setStatus(ExportStatus.FAILED);
                    job.setErrorMessage(ex.getMessage());
                    exportRepository.save(job);
                }
            } catch (Exception saveEx) {
                log.error("[EXPORT-FAIL-SAVE-ERROR] Could not persist FAILED status: {}", saveEx.getMessage());
            }
        } finally {
            // Cleanup temp working directory
            cleanupDir(workDir);
        }
    }

    // ── C. STATUS & DOWNLOAD ───────────────────────────────────────────────

    @Override
    public RasterExportStatusDTO getStatus(UUID exportId) {
        RasterExportJob job = exportRepository.findById(exportId)
                .orElseThrow(() -> new NotFoundException("Export job not found: " + exportId));

        String downloadUrl = null;
        if (job.getStatus() == ExportStatus.COMPLETED && job.getMinioZipPath() != null) {
            try {
                downloadUrl = minioStorageService.createSignedDownloadUrl(
                        exportBucket, job.getMinioZipPath(), 60);
            } catch (Exception ex) {
                log.warn("[EXPORT-STATUS] Could not generate download URL for {}: {}", exportId, ex.getMessage());
            }
        }
        return mapper.toStatus(job, downloadUrl);
    }

    @Override
    public String getDownloadUrl(UUID exportId) {
        RasterExportJob job = exportRepository.findById(exportId)
                .orElseThrow(() -> new NotFoundException("Export job not found: " + exportId));

        if (job.getStatus() != ExportStatus.COMPLETED) {
            throw new RasterExportException(
                    "Export " + exportId + " is not COMPLETED yet — current status: " + job.getStatus());
        }
        try {
            return minioStorageService.createSignedDownloadUrl(
                    exportBucket, job.getMinioZipPath(), 60);
        } catch (Exception ex) {
            throw new RasterExportException("Failed to generate download URL: " + ex.getMessage(), ex);
        }
    }

    // ── Private Helpers ────────────────────────────────────────────────────

    /**
     * Downloads a MinIO object directly to a local file path.
     * Uses MinioStorageService's signed URL to stream bytes to disk.
     */
    private void downloadCogFromMinio(String bucket, String objectPath, Path destination) {
        try {
            // Use MinIO client via MinioStorageService to get object stream
            // MinioStorageService exposes minioClient via constructor injection here,
            // so we use the uploadFile inverse: getObject → write to file
            String signedUrl = minioStorageService.createSignedDownloadUrl(bucket, objectPath, 60);
            try (InputStream in = new java.net.URL(signedUrl).openStream()) {
                Files.copy(in, destination, StandardCopyOption.REPLACE_EXISTING);
            }
            log.info("[EXPORT-DOWNLOAD-COG] Downloaded {} bytes to {}",
                    Files.size(destination), destination);
        } catch (Exception ex) {
            throw new RasterExportException(
                    "Failed to download COG from MinIO: " + ex.getMessage(), ex);
        }
    }

    /** Recursively deletes a temp directory. Errors are logged and swallowed. */
    private void cleanupDir(Path dir) {
        if (dir == null) return;
        try {
            try (var walk = Files.walk(dir)) {
                walk.sorted(java.util.Comparator.reverseOrder())
                        .map(Path::toFile)
                        .forEach(java.io.File::delete);
            }
            log.debug("[EXPORT-CLEANUP] Deleted temp dir: {}", dir);
        } catch (Exception ex) {
            log.warn("[EXPORT-CLEANUP-WARN] Could not fully delete temp dir {}: {}", dir, ex.getMessage());
        }
    }
}


========================================================================================================================
FILE PATH: Orbit_API/geoserver/GeoServerRestService.java
========================================================================================================================

package com.Orbit_API.geoserver;

import com.Orbit_API.catalog.entity.SatelliteImage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

@Slf4j
@Service
public class GeoServerRestService {

    private final RestTemplate restTemplate;

    @Value("${geoserver.base-url}")
    private String baseUrl;

    @Value("${geoserver.workspace}")
    private String workspace;

    // username/password REMOVED — now owned by GeoServerConfig interceptor

    public GeoServerRestService(
            @Qualifier("geoServerRestTemplate") RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public void ensureWorkspace() {
        long startTime = System.currentTimeMillis();
        String url = baseUrl + "/rest/workspaces";

        log.info("[GEOSERVER-WORKSPACE-CREATE] Ensuring workspace exists");
        log.debug("║ Workspace Name : {}", workspace);
        log.debug("║ GeoServer URL  : {}", baseUrl);

        String payload =
                "<workspace>" +
                        "<name>" + workspace + "</name>" +
                        "</workspace>";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_XML);
        HttpEntity<String> request = new HttpEntity<>(payload, headers);

        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    url, HttpMethod.POST, request, String.class);
            long duration = System.currentTimeMillis() - startTime;
            log.info("[GEOSERVER-WORKSPACE-SUCCESS] Workspace ensured");
            log.debug("║ Response Code  : {}", response.getStatusCode());
            log.debug("║ Duration       : {} ms", duration);
        } catch (Exception ex) {
            log.debug("[GEOSERVER-WORKSPACE-EXISTS] Workspace already exists or error: {}",
                    ex.getMessage());
        }
    }

    public void publishCogLayer(SatelliteImage image, String localCogFileUrl) {
        long startTime = System.currentTimeMillis();
        String imageCode = image.getImageCode();

        log.info("[GEOSERVER-PUBLISH-START] Publishing COG layer to GeoServer");
        log.info("║ Image Code     : {}", padRight(imageCode, 63));
        log.info("║ Workspace      : {}", padRight(workspace, 63));
        log.info("║ File URL       : {}", padRight(localCogFileUrl, 63));

        ensureWorkspace();

        // ── STEP 1: Coverage Store ────────────────────────────────────────
        String storeUrl = baseUrl + "/rest/workspaces/" + workspace + "/coveragestores";
        String storeXml =
                "<coverageStore>" +
                        "<name>" + imageCode + "</name>" +
                        "<type>GeoTIFF</type>" +
                        "<enabled>true</enabled>" +
                        "<workspace>" + workspace + "</workspace>" +
                        "<url>" + localCogFileUrl + "</url>" +
                        "</coverageStore>";

        HttpHeaders storeHeaders = new HttpHeaders();
        storeHeaders.setContentType(MediaType.APPLICATION_XML);
        HttpEntity<String> storeRequest = new HttpEntity<>(storeXml, storeHeaders);  // ✅ fixed

        try {
            log.info("║ [STEP 1/2] Creating coverage store...");
            ResponseEntity<String> storeResponse = restTemplate.exchange(
                    storeUrl, HttpMethod.POST, storeRequest, String.class);
            log.info("║ Store Created  : {} ✓", storeResponse.getStatusCode());
        } catch (Exception ex) {
            log.debug("║ Store Already  : Exists or error (OK): {}", ex.getMessage());
        }

        // ── STEP 2: Coverage Layer ────────────────────────────────────────
        String coverageUrl = baseUrl + "/rest/workspaces/" + workspace +
                "/coveragestores/" + imageCode + "/coverages";
        String title = image.getTitle() != null ? image.getTitle() : imageCode;
        String coverageXml =
                "<coverage>" +
                        "<name>" + imageCode + "</name>" +
                        "<title>" + title + "</title>" +
                        "<enabled>true</enabled>" +
                        "<nativeName>" + imageCode + "</nativeName>" +
                        "<nativeCRS>EPSG:4326</nativeCRS>" +
                        "</coverage>";

        HttpHeaders coverageHeaders = new HttpHeaders();
        coverageHeaders.setContentType(MediaType.APPLICATION_XML);
        HttpEntity<String> coverageRequest = new HttpEntity<>(coverageXml, coverageHeaders);  // ✅ fixed

        try {
            log.info("║ [STEP 2/2] Creating coverage layer...");
            ResponseEntity<String> coverageResponse = restTemplate.exchange(
                    coverageUrl, HttpMethod.POST, coverageRequest, String.class);
            log.info("║ Layer Created  : {} ✓", coverageResponse.getStatusCode());
        } catch (Exception ex) {
            log.debug("║ Layer Already  : Exists or error (OK): {}", ex.getMessage());
        }

        long duration = System.currentTimeMillis() - startTime;
        log.info("[GEOSERVER-PUBLISH-SUCCESS] Layer published — {}:{} in {} ms",
                workspace, imageCode, duration);
    }

    public String buildWmsUrl(String layerName) {
        String wmsUrl = baseUrl + "/" + workspace + "/wms";
        log.debug("[GEOSERVER-WMS-URL] WMS URL built: {}", wmsUrl);
        return wmsUrl;
    }

    public String buildWmtsUrl() {
        String wmtsUrl = baseUrl + "/gwc/service/wmts";
        log.debug("[GEOSERVER-WMTS-URL] WMTS URL built: {}", wmtsUrl);
        return wmtsUrl;
    }

    public boolean verifyLayerPublished(String layerName) {
        long startTime = System.currentTimeMillis();
        log.info("[GEOSERVER-VERIFY-START] Verifying layer publication: {}", layerName);

        try {
            String url = baseUrl + "/rest/workspaces/" + workspace +
                    "/layers/" + layerName + ".json";

            HttpHeaders verifyHeaders = new HttpHeaders();
            verifyHeaders.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<String> request = new HttpEntity<>(verifyHeaders);  // ✅ fixed

            ResponseEntity<String> response = restTemplate.exchange(
                    url, HttpMethod.GET, request, String.class);
            long duration = System.currentTimeMillis() - startTime;

            boolean isPublished = response.getStatusCode() == HttpStatus.OK;
            log.info("[GEOSERVER-VERIFY-{}] Layer status: {} in {} ms",
                    isPublished ? "SUCCESS" : "FAILED", isPublished, duration);
            return isPublished;

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.warn("[GEOSERVER-VERIFY-FAILED] {} — {} ms: {}",
                    layerName, duration, ex.getMessage());
            return false;
        }
    }


    /**
     * Deletes a GeoServer coverage layer and its coveragestore for the given imageCode.
     * Sends two DELETE requests:
     *   1. DELETE coverage (the layer itself)
     *   2. DELETE coveragestore with ?recurse=true (removes all remaining references)
     *
     * Both steps are attempted independently — a failure on step 1 still proceeds to step 2.
     *
     * @param imageCode the unique image code used as both store name and coverage name
     */
    public void deleteLayer(String imageCode) {
        log.info("[GEOSERVER-DELETE-START] Deleting layer and store for imageCode={}", imageCode);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_XML);
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        // STEP 1 — Delete the coverage (layer) first
        String coverageUrl = baseUrl + "/rest/workspaces/" + workspace
                + "/coveragestores/" + imageCode
                + "/coverages/" + imageCode;
        try {
            restTemplate.exchange(coverageUrl, HttpMethod.DELETE, requestEntity, String.class);
            log.info("[GEOSERVER-DELETE-COVERAGE] Coverage deleted: {}", coverageUrl);
        } catch (Exception ex) {
            // Coverage may not exist yet (e.g. image stuck at PROCESSING_COMPLETE) — log and continue
            log.warn("[GEOSERVER-DELETE-COVERAGE-WARN] Could not delete coverage at '{}': {}",
                    coverageUrl, ex.getMessage());
        }

        // STEP 2 — Delete the coveragestore with recurse=true (cleans up everything underneath)
        String storeUrl = baseUrl + "/rest/workspaces/" + workspace
                + "/coveragestores/" + imageCode
                + "?recurse=true";
        try {
            restTemplate.exchange(storeUrl, HttpMethod.DELETE, requestEntity, String.class);
            log.info("[GEOSERVER-DELETE-STORE] Coverage store deleted: {}", storeUrl);
        } catch (Exception ex) {
            log.warn("[GEOSERVER-DELETE-STORE-WARN] Could not delete coverage store at '{}': {}",
                    storeUrl, ex.getMessage());
            // Re-throw so the caller (deleteImage) can log and decide — does not break DB delete
            throw new RuntimeException("GeoServer store deletion failed for imageCode=" + imageCode
                    + ": " + ex.getMessage(), ex);
        }

        log.info("[GEOSERVER-DELETE-COMPLETE] Layer and store removed for imageCode={}", imageCode);
    }

    private String padRight(String s, int n) {
        if (s == null) s = "NA";
        return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
    }
}

========================================================================================================================
FILE PATH: Orbit_API/geoserver/ResilientGeoServerService.java
========================================================================================================================

package com.Orbit_API.geoserver;

import com.Orbit_API.catalog.entity.SatelliteImage;
import io.github.resilience4j.retry.annotation.Retry;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class ResilientGeoServerService {

    private final GeoServerRestService geoServerRestService;

    public ResilientGeoServerService(GeoServerRestService geoServerRestService) {
        this.geoServerRestService = geoServerRestService;
    }

    @Retry(name = "geoserver-publish", fallbackMethod = "publishLayerFallback")
    @CircuitBreaker(name = "geoserver", fallbackMethod = "publishLayerFallback")
    public void publishLayerWithRetry(SatelliteImage image, String localCogFileUrl) {
        log.info("Publishing layer to GeoServer: {}", image.getImageCode());
        geoServerRestService.publishCogLayer(image, localCogFileUrl);
    }

    private void publishLayerFallback(SatelliteImage image, String localCogFileUrl, Exception ex) {
        log.error("GeoServer publish failed after retries: {}", image.getImageCode(), ex);
        // Mark for manual retry
    }

    public boolean verifyLayerPublished(String layerName) {
        try {
            return geoServerRestService.verifyLayerPublished(layerName);
        } catch (Exception ex) {
            log.warn("Layer verification failed: {}", layerName, ex);
            return false;
        }
    }
}

========================================================================================================================
FILE PATH: Orbit_API/messaging/config/RabbitMQConfig.java
========================================================================================================================

package com.Orbit_API.messaging.config;


import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.config.SimpleRabbitListenerContainerFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.HashMap;
import java.util.Map;

/**
* RabbitMQ topology for OrbitView:
*
*  orbitview.images (direct exchange, durable)
*    → routing key "image.ingest"         → orbitview.image.ingest          (main queue)
*    → routing key "image.ingest.retry"   → orbitview.image.ingest.retry    (TTL retry queue)
*
*  orbitview.images.dlx (dead-letter exchange, durable)
*    → routing key "image.ingest.dlq"     → orbitview.image.ingest.dlq      (DLQ)
*
*  Main queue dead-letter config:
*    x-dead-letter-exchange   = orbitview.images.dlx
*    x-dead-letter-routing-key = image.ingest.dlq
*
*  Retry queue dead-letter config:
*    x-dead-letter-exchange   = orbitview.images
*    x-dead-letter-routing-key = image.ingest
*    x-message-ttl            = 30000  (30s)
*    This is the "retry trampoline" pattern — message parks in retry queue
*    for TTL ms, then gets re-delivered to main queue.
     */
     @Slf4j
     @Configuration
     public class RabbitMQConfig {

private final RabbitMQProperties props;

public RabbitMQConfig(RabbitMQProperties props) {
this.props = props;
}

// ── Exchanges ────────────────────────────────────────────────────────────

/** Primary direct exchange used for all ingest routing. */
@Bean
public DirectExchange imageIngestExchange() {
return ExchangeBuilder
.directExchange(props.getExchange())
.durable(true)
.build();
}

/** Dead-letter exchange — receives messages that exhaust retries. */
@Bean
public DirectExchange imageDeadLetterExchange() {
return ExchangeBuilder
.directExchange(props.getDlqExchange())
.durable(true)
.build();
}

// ── Queues ───────────────────────────────────────────────────────────────

/**
* Main ingest queue.
* Messages that are nacked without requeue here go to DLX → DLQ directly
* (used only when retry count is exhausted).
  */
  @Bean
  public Queue imageIngestQueue() {
  Map<String, Object> args = new HashMap<>();
  args.put("x-dead-letter-exchange",    props.getDlqExchange());
  args.put("x-dead-letter-routing-key", props.getDlqRoutingKey());
  return QueueBuilder
  .durable(props.getIngestQueue())
  .withArguments(args)
  .build();
  }

/**
* Retry "parking lot" queue.
* Messages sit here for TTL ms, then the DLX re-routes them back to the main queue.
* This implements a delayed retry without a RabbitMQ delayed-message plugin.
  */
  @Bean
  public Queue imageRetryQueue() {
  Map<String, Object> args = new HashMap<>();
  args.put("x-dead-letter-exchange",    props.getExchange());
  args.put("x-dead-letter-routing-key", props.getIngestRoutingKey());
  args.put("x-message-ttl",             props.getRetryTtlMs());
  return QueueBuilder
  .durable(props.getRetryQueue())
  .withArguments(args)
  .build();
  }

/** Dead-letter queue — final resting place for permanently failed messages. */
@Bean
public Queue imageDeadLetterQueue() {
return QueueBuilder
.durable(props.getDlqQueue())
.build();
}

// ── Bindings ─────────────────────────────────────────────────────────────

@Bean
public Binding ingestBinding() {
return BindingBuilder
.bind(imageIngestQueue())
.to(imageIngestExchange())
.with(props.getIngestRoutingKey());
}

@Bean
public Binding retryBinding() {
return BindingBuilder
.bind(imageRetryQueue())
.to(imageIngestExchange())
.with(props.getRetryRoutingKey());
}

@Bean
public Binding dlqBinding() {
return BindingBuilder
.bind(imageDeadLetterQueue())
.to(imageDeadLetterExchange())
.with(props.getDlqRoutingKey());
}

// ── JSON Message Converter ───────────────────────────────────────────────

/**
* Registers Jackson2JsonMessageConverter as the global message converter.
* Enables Spring AMQP to automatically serialize/deserialize DTOs as JSON.
* JavaTimeModule handles LocalDate/LocalDateTime fields.
  */
  @Bean
  public MessageConverter jsonMessageConverter() {
  ObjectMapper mapper = new ObjectMapper();
  mapper.registerModule(new JavaTimeModule());
  mapper.disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  return new Jackson2JsonMessageConverter(mapper);
  }

/**
* RabbitTemplate wired with JSON converter.
* Used by ImageIngestPublisher.
  */
  @Bean
  public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
  RabbitTemplate template = new RabbitTemplate(connectionFactory);
  template.setMessageConverter(jsonMessageConverter());
  template.setMandatory(true); // log unroutable messages
  template.setReturnsCallback(returned ->
  log.error("[RABBIT-UNROUTABLE] message returned: routingKey={} replyText={}",
  returned.getRoutingKey(), returned.getReplyText())
  );
  return template;
  }

/**
* Listener container factory wired with:
* - JSON converter
* - MANUAL acknowledge mode (consumer must ack/nack explicitly)
* - Configurable prefetch and concurrency from RabbitMQProperties
    */
    @Bean
    public SimpleRabbitListenerContainerFactory rabbitListenerContainerFactory(
    ConnectionFactory connectionFactory) {
    SimpleRabbitListenerContainerFactory factory = new SimpleRabbitListenerContainerFactory();
    factory.setConnectionFactory(connectionFactory);
    factory.setMessageConverter(jsonMessageConverter());
    factory.setAcknowledgeMode(AcknowledgeMode.MANUAL);
    factory.setPrefetchCount(props.getPrefetchCount());
    factory.setConcurrentConsumers(props.getConcurrency());
    factory.setMaxConcurrentConsumers(props.getConcurrency() * 2);
    factory.setDefaultRequeueRejected(false); // nack without requeue → goes to DLX
    return factory;
    }
    }


========================================================================================================================
FILE PATH: Orbit_API/messaging/config/RabbitMQProperties.java
========================================================================================================================

package com.Orbit_API.messaging.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
* Centralises all RabbitMQ tuning parameters.
* Bound from application.yml prefix: orbitview.rabbitmq
  */
  @Component
  @ConfigurationProperties(prefix = "orbitview.rabbitmq")
  public class RabbitMQProperties {

  // ── Exchange ────────────────────────────────────────────────────────────
  private String exchange        = "orbitview.images";
  private String exchangeType    = "direct";

  // ── Main Queue ──────────────────────────────────────────────────────────
  private String ingestQueue     = "orbitview.image.ingest";
  private String ingestRoutingKey = "image.ingest";

  // ── Retry Queue (holds nacked messages before re-delivery) ──────────────
  private String retryQueue      = "orbitview.image.ingest.retry";
  private String retryRoutingKey = "image.ingest.retry";
  private long   retryTtlMs      = 30_000L;  // 30s hold before re-queue

  // ── Dead Letter Queue ───────────────────────────────────────────────────
  private String dlqQueue        = "orbitview.image.ingest.dlq";
  private String dlqRoutingKey   = "image.ingest.dlq";
  private String dlqExchange     = "orbitview.images.dlx";

  // ── Consumer Tuning ─────────────────────────────────────────────────────
  private int    prefetchCount   = 1;    // process one at a time per consumer
  private int    concurrency     = 2;    // 2 concurrent listener threads
  private int    maxRetries      = 3;    // before routing to DLQ

  // ── Getters & Setters ───────────────────────────────────────────────────
  public String  getExchange()           { return exchange; }
  public void    setExchange(String v)   { this.exchange = v; }
  public String  getExchangeType()       { return exchangeType; }
  public void    setExchangeType(String v) { this.exchangeType = v; }
  public String  getIngestQueue()        { return ingestQueue; }
  public void    setIngestQueue(String v){ this.ingestQueue = v; }
  public String  getIngestRoutingKey()   { return ingestRoutingKey; }
  public void    setIngestRoutingKey(String v) { this.ingestRoutingKey = v; }
  public String  getRetryQueue()         { return retryQueue; }
  public void    setRetryQueue(String v) { this.retryQueue = v; }
  public String  getRetryRoutingKey()    { return retryRoutingKey; }
  public void    setRetryRoutingKey(String v) { this.retryRoutingKey = v; }
  public long    getRetryTtlMs()         { return retryTtlMs; }
  public void    setRetryTtlMs(long v)   { this.retryTtlMs = v; }
  public String  getDlqQueue()           { return dlqQueue; }
  public void    setDlqQueue(String v)   { this.dlqQueue = v; }
  public String  getDlqRoutingKey()      { return dlqRoutingKey; }
  public void    setDlqRoutingKey(String v) { this.dlqRoutingKey = v; }
  public String  getDlqExchange()        { return dlqExchange; }
  public void    setDlqExchange(String v){ this.dlqExchange = v; }
  public int     getPrefetchCount()      { return prefetchCount; }
  public void    setPrefetchCount(int v) { this.prefetchCount = v; }
  public int     getConcurrency()        { return concurrency; }
  public void    setConcurrency(int v)   { this.concurrency = v; }
  public int     getMaxRetries()         { return maxRetries; }
  public void    setMaxRetries(int v)    { this.maxRetries = v; }
  }


========================================================================================================================
FILE PATH: Orbit_API/messaging/consumer/ImageIngestConsumer.java
========================================================================================================================

package com.Orbit_API.messaging.consumer;


import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.geoserver.GeoServerRestService;
import com.Orbit_API.messaging.config.RabbitMQProperties;
import com.Orbit_API.messaging.dto.ImageIngestMessageDTO;
import com.Orbit_API.messaging.entity.ImageProcessingJob;
import com.Orbit_API.messaging.enums.JobStatus;
import com.Orbit_API.messaging.enums.ProcessingStage;
import com.Orbit_API.messaging.exception.MessageProcessingException;
import com.Orbit_API.messaging.repository.ImageProcessingJobRepository;
import com.Orbit_API.processing.GdalProcessingService;
import com.Orbit_API.storage.MinioStorageService;
import com.fasterxml.jackson.databind.JsonNode;
import com.rabbitmq.client.Channel;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Polygon;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.context.annotation.Lazy;
import org.springframework.amqp.rabbit.core.RabbitTemplate;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.*;

/**
* RabbitMQ consumer for image ingest jobs.
*
* Listens on: orbitview.image.ingest queue
* Ack mode:   MANUAL — ack only on full success, nack on failure
*
* Retry strategy:
*   - recoverable failure → increment retryCount, re-publish to retry queue
*   - retry queue holds message for TTL ms then re-delivers to main queue
*   - when retryCount >= maxRetries → nack (message goes to DLQ)
*   - satellite_images.status and job.status both updated to FAILED
*
* Idempotency:
*   - loads ImageProcessingJob by jobId
*   - if job.status is PUBLISHED or DEAD_LETTERED → ack and skip (already done)
*   - if job.status is FAILED and retryCount >= maxRetries → ack and skip
      */
      @Slf4j
      @Service
      public class ImageIngestConsumer {

private final SatelliteImageRepository    imageRepository;
private final ImageProcessingJobRepository jobRepository;
private final GdalProcessingService       gdalService;
private final MinioStorageService         minioService;
private final GeoServerRestService        geoServerService;
private final RabbitMQProperties          props;
private final RabbitTemplate rabbitTemplate;   // ← ADD THIS FIELD

@Value("${minio.bucket-raw}")
private String rawBucket;

@Value("${minio.bucket-cog}")
private String cogBucket;

@Value("${app.upload.temp-dir:/tmp/orbitview}")
private String tempDirectory;

@Value("${orbitview.shared-data-dir}")
private String sharedDataDir;

@Value("${geoserver.publish.retry-attempts:3}")
private int geoServerRetryAttempts;

public ImageIngestConsumer(SatelliteImageRepository imageRepository,
ImageProcessingJobRepository jobRepository,
GdalProcessingService gdalService,
MinioStorageService minioService,
GeoServerRestService geoServerService,
RabbitMQProperties props,
@Lazy RabbitTemplate rabbitTemplate) {
this.imageRepository = imageRepository;
this.jobRepository   = jobRepository;
this.gdalService     = gdalService;
this.minioService    = minioService;
this.geoServerService = geoServerService;
this.props           = props;
this.rabbitTemplate  = rabbitTemplate;
}

/**
* Main consumer listener.
* containerFactory matches the bean name in RabbitMQConfig.
  */
  @RabbitListener(
  queues       = "#{rabbitMQProperties.ingestQueue}",
  containerFactory = "rabbitListenerContainerFactory",
  ackMode      = "MANUAL"
  )
  public void onMessage(ImageIngestMessageDTO msg,
  Channel channel,
  @Header(AmqpHeaders.DELIVERY_TAG) long deliveryTag) {
  String correlationId = msg.getCorrelationId();
  String imageCode     = msg.getImageCode();

  log.info("[CONSUMER-RECEIVED] imageCode={} correlationId={} retryCount={}/{}",
  imageCode, correlationId, msg.getRetryCount(), msg.getMaxRetries());

  // ── Idempotency guard ───────────────────────────────────────────────
  Optional<ImageProcessingJob> jobOpt = jobRepository.findById(msg.getJobId());
  if (jobOpt.isPresent()) {
  ImageProcessingJob job = jobOpt.get();
  if (job.getStatus() == JobStatus.PUBLISHED) {
  log.info("[CONSUMER-SKIP] Already PUBLISHED — acking duplicate. imageCode={}", imageCode);
  ackQuietly(channel, deliveryTag, correlationId);
  return;
  }
  if (job.getStatus() == JobStatus.DEAD_LETTERED) {
  log.info("[CONSUMER-SKIP] Already DEAD_LETTERED — acking. imageCode={}", imageCode);
  ackQuietly(channel, deliveryTag, correlationId);
  return;
  }
  }

  Path tempDir = null;
  try {
  // ── Mark RECEIVED ───────────────────────────────────────────────
  updateJobStatus(msg.getJobId(), JobStatus.RECEIVED,
  ProcessingStage.MESSAGE_RECEIVED, null, null);

       SatelliteImage image = imageRepository.findById(msg.getImageId())
               .orElseThrow(() -> new MessageProcessingException(
                       "Image not found in DB: " + msg.getImageId(),
                       "DB_LOOKUP", false));

       image.setStatus(ImageProcessingStatus.PROCESSING.name());
       imageRepository.save(image);
       updateJobStatus(msg.getJobId(), JobStatus.PROCESSING,
               ProcessingStage.GDAL_METADATA_EXTRACTION, null, null);

       // ── STEP 1: Download raw from MinIO to temp dir ─────────────────
       tempDir = Files.createDirectories(
               Path.of(tempDirectory, "consumer", imageCode));
       Path tempRaw = downloadRawFromMinio(msg, tempDir, correlationId);

       // ── STEP 2: GDAL metadata + footprint ───────────────────────────
       log.info("[CONSUMER-STEP-2] GDAL metadata extraction. correlationId={}", correlationId);
       JsonNode gdalJson = gdalService.runGdalInfoJson(tempRaw);
       int epsgCode      = gdalService.extractEpsgCode(gdalJson);
       Polygon footprint = gdalService.buildFootprintFromGdalJson(gdalJson);
       image.setCrsEpsg(epsgCode);
       image.setFootprint(footprint);
       imageRepository.save(image);
       updateJobStatus(msg.getJobId(), JobStatus.PROCESSING,
               ProcessingStage.COG_CONVERSION, null, null);

       // ── STEP 3: Convert to COG ──────────────────────────────────────
       log.info("[CONSUMER-STEP-3] COG conversion. correlationId={}", correlationId);
       Path tempCog = tempDir.resolve(imageCode + "_cog.tif");
       gdalService.convertToCog(tempRaw, tempCog);

       // ── STEP 4: Upload COG to MinIO ─────────────────────────────────
       log.info("[CONSUMER-STEP-4] Uploading COG to MinIO. correlationId={}", correlationId);
       String cogObjectPath = "cog/" + imageCode + "/processed.tif";
       uploadToMinioWithRetry(cogBucket, cogObjectPath, tempCog, "image/tiff", correlationId);
       image.setCogObjectPath(cogObjectPath);
       imageRepository.save(image);
       updateJobStatus(msg.getJobId(), JobStatus.PROCESSING,
               ProcessingStage.MINIO_COG_UPLOAD, cogObjectPath, null);

       // ── STEP 5: Copy COG to GeoServer shared dir ────────────────────
       log.info("[CONSUMER-STEP-5] Copying COG to GeoServer shared dir. correlationId={}", correlationId);
       Path sharedCogFile = copyToGeoServerDirectory(tempCog, imageCode);
       image.setStatus(ImageProcessingStatus.PROCESSING_COMPLETE.name());
       imageRepository.save(image);
       updateJobStatus(msg.getJobId(), JobStatus.PROCESSING_COMPLETE,
               ProcessingStage.GEOSERVER_PUBLISH, null, null);

       // ── STEP 6: Publish to GeoServer ─────────────────────────────────
       log.info("[CONSUMER-STEP-6] Publishing to GeoServer. correlationId={}", correlationId);
       String fileUrl = "file://" + sharedCogFile.toAbsolutePath().toString().replace("\\", "/");
       publishToGeoServerWithRetry(image, imageCode, fileUrl, correlationId);

       // ── STEP 7: Finalize job ──────────────────────────────────────────
       ImageProcessingJob job = jobRepository.findById(msg.getJobId())
               .orElseGet(ImageProcessingJob::new);
       job.setStatus(JobStatus.PUBLISHED);
       job.setStage(ProcessingStage.COMPLETE);
       job.setCogObjectPath(cogObjectPath);
       job.setFinishedAt(LocalDateTime.now());
       jobRepository.save(job);

       log.info("[CONSUMER-SUCCESS] imageCode={} correlationId={} epsg={} layer={}",
               imageCode, correlationId, epsgCode, image.getGeoserverLayerName());

       // ── ACK ───────────────────────────────────────────────────────────
       channel.basicAck(deliveryTag, false);
       log.info("[CONSUMER-ACK] deliveryTag={} imageCode={}", deliveryTag, imageCode);

  } catch (MessageProcessingException ex) {
  log.error("[CONSUMER-PIPELINE-ERROR] stage={} recoverable={} imageCode={} correlationId={} error={}",
  ex.getStage(), ex.isRecoverable(), imageCode, correlationId, ex.getMessage(), ex);
  handleFailure(msg, channel, deliveryTag, ex.getStage(), ex.getMessage(),
  ex.isRecoverable(), tempDir);

  } catch (Exception ex) {
  log.error("[CONSUMER-UNEXPECTED-ERROR] imageCode={} correlationId={} error={}",
  imageCode, correlationId, ex.getMessage(), ex);
  handleFailure(msg, channel, deliveryTag, "UNKNOWN", ex.getMessage(), true, tempDir);
  }
  }

// ── Failure handler ──────────────────────────────────────────────────────

private void handleFailure(ImageIngestMessageDTO msg,
Channel channel,
long deliveryTag,
String failedStage,
String errorMessage,
boolean recoverable,
Path tempDir) {
String correlationId = msg.getCorrelationId();
String imageCode     = msg.getImageCode();

     // Update satellite_images status
     try {
         imageRepository.findById(msg.getImageId()).ifPresent(image -> {
             image.setStatus(ImageProcessingStatus.FAILED.name());
             imageRepository.save(image);
         });
     } catch (Exception e) {
         log.error("[CONSUMER-FAIL-DB] Could not update image status: {}", e.getMessage());
     }

     boolean canRetry = recoverable
             && (msg.getRetryCount() < msg.getMaxRetries());

     if (canRetry) {
         int newRetryCount = msg.getRetryCount() + 1;
         log.warn("[CONSUMER-RETRY] Scheduling retry {}/{} imageCode={} correlationId={}",
                 newRetryCount, msg.getMaxRetries(), imageCode, correlationId);

         // Update job row
         updateJobStatusWithError(msg.getJobId(), JobStatus.FAILED,
                 ProcessingStage.FAILED, failedStage, errorMessage);

         // Re-publish to retry queue with incremented retryCount
         msg.setRetryCount(newRetryCount);
         try {
             // We send directly to retry queue — it will TTL-expire back to main queue
             // We need a RabbitTemplate here — injected via field
             rabbitTemplate.convertAndSend(          // ← uses the injected field directly
                     props.getExchange(),
                     props.getRetryRoutingKey(),
                     msg);
             log.info("[CONSUMER-RETRY-PUBLISHED] retry queue imageCode={} correlationId={}",
                     imageCode, correlationId);
         } catch (Exception ex) {
             log.error("[CONSUMER-RETRY-PUBLISH-FAIL] {}", ex.getMessage(), ex);
         }

         // ACK the current delivery (we're handling retry manually)
         ackQuietly(channel, deliveryTag, correlationId);

     } else {
         log.error("[CONSUMER-DLQ] Exhausted retries or non-recoverable. Sending to DLQ. imageCode={} correlationId={}",
                 imageCode, correlationId);
         updateJobStatusWithError(msg.getJobId(), JobStatus.DEAD_LETTERED,
                 ProcessingStage.FAILED, failedStage, errorMessage);
         // NACK without requeue → goes to DLX → DLQ
         nackQuietly(channel, deliveryTag, false, correlationId);
     }

     cleanupTempDir(tempDir);
}

// ── Processing helpers ───────────────────────────────────────────────────

private Path downloadRawFromMinio(ImageIngestMessageDTO msg, Path tempDir, String correlationId)
throws Exception {
String filename = msg.getOriginalFileName() != null
? msg.getOriginalFileName() : msg.getImageCode() + ".tif";
// Derive extension from rawObjectPath
String rawPath = msg.getRawObjectPath();
if (rawPath != null && rawPath.contains(".")) {
filename = rawPath.substring(rawPath.lastIndexOf('/') + 1);
}
Path localFile = tempDir.resolve(filename);

     log.debug("[CONSUMER-MINIO-DOWNLOAD] bucket={} path={} correlationId={}",
             msg.getRawBucket(), msg.getRawObjectPath(), correlationId);
     try (InputStream stream = minioService.downloadObject(
             msg.getRawBucket(), msg.getRawObjectPath())) {
         Files.copy(stream, localFile, StandardCopyOption.REPLACE_EXISTING);
     }
     log.info("[CONSUMER-MINIO-DOWNLOAD-OK] localFile={} size={} correlationId={}",
             localFile, Files.size(localFile), correlationId);
     return localFile;
}

private void uploadToMinioWithRetry(String bucket, String path, Path file,
String contentType, String correlationId) {
int maxAttempts = 3;
for (int attempt = 1; attempt <= maxAttempts; attempt++) {
try (InputStream stream = Files.newInputStream(file)) {
minioService.upload(bucket, path, stream, Files.size(file), contentType);
log.info("[CONSUMER-MINIO-UPLOAD-OK] path={} attempt={} correlationId={}",
path, attempt, correlationId);
return;
} catch (Exception ex) {
log.warn("[CONSUMER-MINIO-UPLOAD-RETRY] attempt={}/{} path={} error={}",
attempt, maxAttempts, path, ex.getMessage());
if (attempt == maxAttempts) {
throw new MessageProcessingException(
"MinIO upload failed after " + maxAttempts + " attempts: " + ex.getMessage(),
"MINIO_UPLOAD", true, ex);
}
sleepQuietly(2000L * attempt);
}
}
}

private Path copyToGeoServerDirectory(Path cogFile, String imageCode) throws Exception {
Path targetDir  = Files.createDirectories(Path.of(sharedDataDir, "cogs", imageCode));
Path targetFile = targetDir.resolve("processed.tif");
Files.copy(cogFile, targetFile, StandardCopyOption.REPLACE_EXISTING);
log.info("[CONSUMER-GEOSERVER-COPY] copied to {}", targetFile);
return targetFile;
}

private void publishToGeoServerWithRetry(SatelliteImage image, String imageCode,
String fileUrl, String correlationId) {
for (int attempt = 1; attempt <= geoServerRetryAttempts; attempt++) {
try {
geoServerService.publishCogLayer(image, fileUrl);
image.setGeoserverLayerName("satellite-portal:" + imageCode);
image.setGeoserverWmsUrl(geoServerService.buildWmsUrl(image.getGeoserverLayerName()));
image.setGeoserverWmtsUrl(geoServerService.buildWmtsUrl());
image.setStatus(ImageProcessingStatus.PUBLISHED.name());
imageRepository.save(image);
log.info("[CONSUMER-GEOSERVER-PUBLISH-OK] attempt={} layer={} correlationId={}",
attempt, image.getGeoserverLayerName(), correlationId);
return;
} catch (Exception ex) {
log.warn("[CONSUMER-GEOSERVER-RETRY] attempt={}/{} error={}",
attempt, geoServerRetryAttempts, ex.getMessage());
if (attempt == geoServerRetryAttempts) {
image.setStatus(ImageProcessingStatus.PUBLISHED_FAILED.name());
imageRepository.save(image);
// Published_failed is non-recoverable for retry (image is in DB, just no WMS)
throw new MessageProcessingException(
"GeoServer publish failed after " + geoServerRetryAttempts + " attempts",
"GEOSERVER_PUBLISH", false, ex);
}
sleepQuietly(2000L * attempt);
}
}
}

// ── Job status helpers ───────────────────────────────────────────────────

@Transactional
private void updateJobStatus(UUID jobId, JobStatus status,
ProcessingStage stage,
String cogPath, String errorMessage) {
jobRepository.findById(jobId).ifPresent(job -> {
job.setStatus(status);
job.setStage(stage);
if (cogPath     != null) job.setCogObjectPath(cogPath);
if (errorMessage != null) job.setErrorMessage(errorMessage);
if (status == JobStatus.RECEIVED) job.setStartedAt(LocalDateTime.now());
jobRepository.save(job);
});
}

@Transactional
private void updateJobStatusWithError(UUID jobId, JobStatus status,
ProcessingStage stage,
String failedStage, String errorMessage) {
jobRepository.findById(jobId).ifPresent(job -> {
job.setStatus(status);
job.setStage(stage);
job.setFailedStage(failedStage);
job.setErrorMessage(errorMessage);
job.setFinishedAt(LocalDateTime.now());
job.setRetryCount(job.getRetryCount() + 1);
jobRepository.save(job);
});
}

// ── ACK/NACK helpers ─────────────────────────────────────────────────────

private void ackQuietly(Channel channel, long deliveryTag, String correlationId) {
try {
channel.basicAck(deliveryTag, false);
log.debug("[CONSUMER-ACK] deliveryTag={} correlationId={}", deliveryTag, correlationId);
} catch (IOException ex) {
log.error("[CONSUMER-ACK-FAIL] deliveryTag={} error={}", deliveryTag, ex.getMessage());
}
}

private void nackQuietly(Channel channel, long deliveryTag,
boolean requeue, String correlationId) {
try {
channel.basicNack(deliveryTag, false, requeue);
log.debug("[CONSUMER-NACK] deliveryTag={} requeue={} correlationId={}",
deliveryTag, requeue, correlationId);
} catch (IOException ex) {
log.error("[CONSUMER-NACK-FAIL] deliveryTag={} error={}", deliveryTag, ex.getMessage());
}
}

private void cleanupTempDir(Path dir) {
if (dir == null) return;
try (var walk = Files.walk(dir)) {
walk.sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(java.io.File::delete);
} catch (Exception ex) {
log.warn("[CONSUMER-CLEANUP] Could not clean temp dir {}: {}", dir, ex.getMessage());
}
}

private void sleepQuietly(long ms) {
try { Thread.sleep(ms); } catch (InterruptedException ie) {
Thread.currentThread().interrupt();
}
}
}


========================================================================================================================
FILE PATH: Orbit_API/messaging/consumer/ImageIngestDlqConsumer.java
========================================================================================================================

package com.Orbit_API.messaging.consumer;



import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.messaging.dto.ImageIngestMessageDTO;
import com.Orbit_API.messaging.enums.JobStatus;
import com.Orbit_API.messaging.enums.ProcessingStage;
import com.Orbit_API.messaging.repository.ImageProcessingJobRepository;
import com.rabbitmq.client.Channel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.AmqpHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.time.LocalDateTime;

/**
* DLQ consumer — handles messages that exhausted all retries.
* Marks the satellite image and processing job as permanently FAILED.
* Acks the DLQ message so it does not block the DLQ indefinitely.
* An operator can inspect this queue for manual replay or investigation.
  */
  @Slf4j
  @Service
  public class ImageIngestDlqConsumer {

  private final SatelliteImageRepository    imageRepository;
  private final ImageProcessingJobRepository jobRepository;

  public ImageIngestDlqConsumer(SatelliteImageRepository imageRepository,
  ImageProcessingJobRepository jobRepository) {
  this.imageRepository = imageRepository;
  this.jobRepository   = jobRepository;
  }

  @RabbitListener(
  queues           = "#{rabbitMQProperties.dlqQueue}",
  containerFactory = "rabbitListenerContainerFactory",
  ackMode          = "MANUAL"
  )
  @Transactional
  public void onDlqMessage(ImageIngestMessageDTO msg,
  Channel channel,
  @Header(AmqpHeaders.DELIVERY_TAG) long deliveryTag) {
  String imageCode     = msg.getImageCode();
  String correlationId = msg.getCorrelationId();

       log.error("[DLQ-RECEIVED] imageCode={} correlationId={} retryCount={} jobId={}",
               imageCode, correlationId, msg.getRetryCount(), msg.getJobId());

       // 1. Mark satellite_images as FAILED
       try {
           imageRepository.findById(msg.getImageId()).ifPresent(image -> {
               image.setStatus(ImageProcessingStatus.FAILED.name());
               imageRepository.save(image);
               log.error("[DLQ-IMAGE-FAILED] imageCode={} imageId={}", imageCode, msg.getImageId());
           });
       } catch (Exception ex) {
           log.error("[DLQ-IMAGE-FAIL-ERROR] {}", ex.getMessage());
       }

       // 2. Mark job as DEAD_LETTERED
       try {
           jobRepository.findById(msg.getJobId()).ifPresent(job -> {
               job.setStatus(JobStatus.DEAD_LETTERED);
               job.setStage(ProcessingStage.FAILED);
               job.setErrorMessage("Exhausted " + msg.getMaxRetries() + " retries. Moved to DLQ.");
               job.setFinishedAt(LocalDateTime.now());
               jobRepository.save(job);
               log.error("[DLQ-JOB-DEAD-LETTERED] jobId={} imageCode={}", job.getId(), imageCode);
           });
       } catch (Exception ex) {
           log.error("[DLQ-JOB-FAIL-ERROR] {}", ex.getMessage());
       }

       // 3. ACK DLQ message so it is consumed (operator can check DB for FAILED records)
       try {
           channel.basicAck(deliveryTag, false);
           log.info("[DLQ-ACK] deliveryTag={} imageCode={} correlationId={}",
                   deliveryTag, imageCode, correlationId);
       } catch (IOException ex) {
           log.error("[DLQ-ACK-FAIL] {}", ex.getMessage());
       }
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/messaging/dto/ImageIngestMessageDTO.java
========================================================================================================================

package com.Orbit_API.messaging.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

/**
* RabbitMQ message payload for satellite image ingest jobs.
*
* DESIGN RULES:
* - Contains ONLY IDs, paths, and metadata. Never file bytes.
* - rawObjectPath points to the already-uploaded MinIO object.
* - Consumer reads the file from MinIO using rawObjectPath.
* - Must remain serializable as JSON by Jackson.
    */
    @JsonIgnoreProperties(ignoreUnknown = true)
    public class ImageIngestMessageDTO implements Serializable {

private UUID          jobId;
private UUID          imageId;
private String        imageCode;
private String        userId;
private String        correlationId;
private String        uploadMode;          // SINGLE_FILE_MODE / SENTINEL_RGB_MODE / etc.

// ── File pointer (consumer downloads from MinIO) ─────────────────────────
private String        rawObjectPath;       // e.g. "raw/IMG-xxx/image.tif"
private String        rawBucket;           // e.g. "orbitview-raw-images"
private String        originalFileName;

// ── Image metadata ───────────────────────────────────────────────────────
private String        title;
private String        satelliteName;
private String        sensorName;
private String        processingLevel;
private LocalDate     acquisitionDate;
private Double        cloudCover;
private Double        resolutionM;

// ── Sentinel-2 specific ──────────────────────────────────────────────────
private String        bandManifestJson;
private String        sourceProductName;
private String        tileId;

// ── Retry tracking ───────────────────────────────────────────────────────
private int           retryCount;
private int           maxRetries;

private LocalDateTime requestedAt;

// ── Getters & Setters ────────────────────────────────────────────────────
public UUID          getJobId()                     { return jobId; }
public void          setJobId(UUID v)               { this.jobId = v; }
public UUID          getImageId()                   { return imageId; }
public void          setImageId(UUID v)             { this.imageId = v; }
public String        getImageCode()                 { return imageCode; }
public void          setImageCode(String v)         { this.imageCode = v; }
public String        getUserId()                    { return userId; }
public void          setUserId(String v)            { this.userId = v; }
public String        getCorrelationId()             { return correlationId; }
public void          setCorrelationId(String v)     { this.correlationId = v; }
public String        getUploadMode()                { return uploadMode; }
public void          setUploadMode(String v)        { this.uploadMode = v; }
public String        getRawObjectPath()             { return rawObjectPath; }
public void          setRawObjectPath(String v)     { this.rawObjectPath = v; }
public String        getRawBucket()                 { return rawBucket; }
public void          setRawBucket(String v)         { this.rawBucket = v; }
public String        getOriginalFileName()          { return originalFileName; }
public void          setOriginalFileName(String v)  { this.originalFileName = v; }
public String        getTitle()                     { return title; }
public void          setTitle(String v)             { this.title = v; }
public String        getSatelliteName()             { return satelliteName; }
public void          setSatelliteName(String v)     { this.satelliteName = v; }
public String        getSensorName()                { return sensorName; }
public void          setSensorName(String v)        { this.sensorName = v; }
public String        getProcessingLevel()           { return processingLevel; }
public void          setProcessingLevel(String v)   { this.processingLevel = v; }
public LocalDate     getAcquisitionDate()           { return acquisitionDate; }
public void          setAcquisitionDate(LocalDate v){ this.acquisitionDate = v; }
public Double        getCloudCover()                { return cloudCover; }
public void          setCloudCover(Double v)        { this.cloudCover = v; }
public Double        getResolutionM()               { return resolutionM; }
public void          setResolutionM(Double v)       { this.resolutionM = v; }
public String        getBandManifestJson()          { return bandManifestJson; }
public void          setBandManifestJson(String v)  { this.bandManifestJson = v; }
public String        getSourceProductName()         { return sourceProductName; }
public void          setSourceProductName(String v) { this.sourceProductName = v; }
public String        getTileId()                    { return tileId; }
public void          setTileId(String v)            { this.tileId = v; }
public int           getRetryCount()                { return retryCount; }
public void          setRetryCount(int v)           { this.retryCount = v; }
public int           getMaxRetries()                { return maxRetries; }
public void          setMaxRetries(int v)           { this.maxRetries = v; }
public LocalDateTime getRequestedAt()               { return requestedAt; }
public void          setRequestedAt(LocalDateTime v){ this.requestedAt = v; }
}


========================================================================================================================
FILE PATH: Orbit_API/messaging/entity/ImageProcessingJob.java
========================================================================================================================

package com.Orbit_API.messaging.entity;


import com.Orbit_API.messaging.enums.JobStatus;
import com.Orbit_API.messaging.enums.ProcessingStage;
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

/**
* Persistent record of one RabbitMQ-driven image processing job.
*
* Lifecycle mirrors the consumer pipeline steps.
* retryCount is incremented by the consumer before re-publishing to the retry queue.
* When retryCount >= maxRetries, the message is nacked to go to the DLQ and
* this row is updated to DEAD_LETTERED.
  */
  @Entity
  @Table(
  name = "image_processing_jobs",
  indexes = {
  @Index(name = "idx_ipj_image_id",       columnList = "image_id"),
  @Index(name = "idx_ipj_status",          columnList = "status"),
  @Index(name = "idx_ipj_correlation_id",  columnList = "correlation_id"),
  @Index(name = "idx_ipj_created_at",      columnList = "created_at")
  }
  )
  public class ImageProcessingJob {

  @Id
  @GeneratedValue(strategy = GenerationType.UUID)
  @Column(updatable = false, nullable = false)
  private UUID id;

//    @Version
//    private Long version;

    @Column(name = "image_id", nullable = false)
    private UUID imageId;

    @Column(name = "image_code", nullable = false)
    private String imageCode;

    @Column(name = "job_type", nullable = false)
    private String jobType;           // e.g. IMAGE_INGEST

    @Column(name = "queue_name")
    private String queueName;

    @Column(name = "routing_key")
    private String routingKey;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private JobStatus status;

    @Enumerated(EnumType.STRING)
    @Column(name = "stage")
    private ProcessingStage stage;

    @Column(name = "retry_count")
    private int retryCount;

    @Column(name = "max_retries")
    private int maxRetries;

    @Column(name = "correlation_id")
    private String correlationId;

    @Column(name = "requested_by")
    private String requestedBy;

    @Column(name = "raw_object_path")
    private String rawObjectPath;

    @Column(name = "cog_object_path")
    private String cogObjectPath;

    @Column(name = "preview_png_path")
    private String previewPngPath;

    @Column(name = "preview_jpeg_path")
    private String previewJpegPath;

    @Column(name = "metadata_json", columnDefinition = "TEXT")
    private String metadataJson;     // serialized message DTO for audit

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @Column(name = "failed_stage")
    private String failedStage;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "started_at")
    private LocalDateTime startedAt;

    @Column(name = "finished_at")
    private LocalDateTime finishedAt;

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    // ── Getters & Setters ────────────────────────────────────────────────────
    public UUID             getId()                        { return id; }
    public void             setId(UUID v)                  { this.id = v; }
    public UUID             getImageId()                   { return imageId; }
    public void             setImageId(UUID v)             { this.imageId = v; }
    public String           getImageCode()                 { return imageCode; }
    public void             setImageCode(String v)         { this.imageCode = v; }
    public String           getJobType()                   { return jobType; }
    public void             setJobType(String v)           { this.jobType = v; }
    public String           getQueueName()                 { return queueName; }
    public void             setQueueName(String v)         { this.queueName = v; }
    public String           getRoutingKey()                { return routingKey; }
    public void             setRoutingKey(String v)        { this.routingKey = v; }
    public JobStatus        getStatus()                    { return status; }
    public void             setStatus(JobStatus v)         { this.status = v; }
    public ProcessingStage  getStage()                     { return stage; }
    public void             setStage(ProcessingStage v)    { this.stage = v; }
    public int              getRetryCount()                { return retryCount; }
    public void             setRetryCount(int v)           { this.retryCount = v; }
    public int              getMaxRetries()                { return maxRetries; }
    public void             setMaxRetries(int v)           { this.maxRetries = v; }
    public String           getCorrelationId()             { return correlationId; }
    public void             setCorrelationId(String v)     { this.correlationId = v; }
    public String           getRequestedBy()               { return requestedBy; }
    public void             setRequestedBy(String v)       { this.requestedBy = v; }
    public String           getRawObjectPath()             { return rawObjectPath; }
    public void             setRawObjectPath(String v)     { this.rawObjectPath = v; }
    public String           getCogObjectPath()             { return cogObjectPath; }
    public void             setCogObjectPath(String v)     { this.cogObjectPath = v; }
    public String           getPreviewPngPath()            { return previewPngPath; }
    public void             setPreviewPngPath(String v)    { this.previewPngPath = v; }
    public String           getPreviewJpegPath()           { return previewJpegPath; }
    public void             setPreviewJpegPath(String v)   { this.previewJpegPath = v; }
    public String           getMetadataJson()              { return metadataJson; }
    public void             setMetadataJson(String v)      { this.metadataJson = v; }
    public String           getErrorMessage()              { return errorMessage; }
    public void             setErrorMessage(String v)      { this.errorMessage = v; }
    public String           getFailedStage()               { return failedStage; }
    public void             setFailedStage(String v)       { this.failedStage = v; }
    public LocalDateTime    getCreatedAt()                 { return createdAt; }
    public void             setCreatedAt(LocalDateTime v)  { this.createdAt = v; }
    public LocalDateTime    getUpdatedAt()                 { return updatedAt; }
    public void             setUpdatedAt(LocalDateTime v)  { this.updatedAt = v; }
    public LocalDateTime    getStartedAt()                 { return startedAt; }
    public void             setStartedAt(LocalDateTime v)  { this.startedAt = v; }
    public LocalDateTime    getFinishedAt()                { return finishedAt; }
    public void             setFinishedAt(LocalDateTime v) { this.finishedAt = v; }
}


========================================================================================================================
FILE PATH: Orbit_API/messaging/enums/JobStatus.java
========================================================================================================================

package com.Orbit_API.messaging.enums;



/**
* Lifecycle of an ImageProcessingJob row.
*
* QUEUED            — row created, message published to RabbitMQ
* RECEIVED          — consumer picked up the message
* PROCESSING        — heavy pipeline running
* PROCESSING_COMPLETE — COG uploaded, GeoServer copy done
* PUBLISHED         — GeoServer WMS/WMTS layer created successfully
* PUBLISHED_FAILED  — GeoServer publish failed all retries
* FAILED            — pipeline exception, satellite_images.status = FAILED
* DEAD_LETTERED     — exhausted all retries, moved to DLQ
  */
  public enum JobStatus {
  QUEUED,
  RECEIVED,
  PROCESSING,
  PROCESSING_COMPLETE,
  PUBLISHED,
  PUBLISHED_FAILED,
  FAILED,
  DEAD_LETTERED
  }


========================================================================================================================
FILE PATH: Orbit_API/messaging/enums/ProcessingStage.java
========================================================================================================================

package com.Orbit_API.messaging.enums;



/**
* Fine-grained stages within the consumer pipeline.
* Used in ImageProcessingJob.stage for detailed progress display.
  */
  public enum ProcessingStage {
  QUEUED_FOR_PROCESSING,
  MESSAGE_RECEIVED,
  GDAL_METADATA_EXTRACTION,
  FOOTPRINT_BUILDING,
  COG_CONVERSION,
  PREVIEW_GENERATION,
  MINIO_RAW_UPLOAD,
  MINIO_COG_UPLOAD,
  MINIO_PREVIEW_UPLOAD,
  GEOSERVER_COPY,
  GEOSERVER_PUBLISH,
  COMPLETE,
  FAILED
  }


========================================================================================================================
FILE PATH: Orbit_API/messaging/exception/MessageProcessingException.java
========================================================================================================================

package com.Orbit_API.messaging.exception;


/**
* Thrown inside the RabbitMQ consumer pipeline when a recoverable or
* unrecoverable processing error occurs.
*
* recoverable=true  → consumer will increment retryCount and re-publish to retry queue
* recoverable=false → consumer will nack without requeue → DLQ
  */
  public class MessageProcessingException extends RuntimeException {

  private final boolean recoverable;
  private final String  stage;

  public MessageProcessingException(String message, String stage, boolean recoverable) {
  super(message);
  this.stage       = stage;
  this.recoverable = recoverable;
  }

  public MessageProcessingException(String message, String stage, boolean recoverable, Throwable cause) {
  super(message, cause);
  this.stage       = stage;
  this.recoverable = recoverable;
  }

  public boolean isRecoverable() { return recoverable; }
  public String  getStage()      { return stage; }
  }


========================================================================================================================
FILE PATH: Orbit_API/messaging/mapper/ImageIngestMessageMapper.java
========================================================================================================================

package com.Orbit_API.messaging.mapper;

import com.Orbit_API.catalog.dto.UploadImageRequest;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.messaging.dto.ImageIngestMessageDTO;
import com.Orbit_API.messaging.entity.ImageProcessingJob;
import com.Orbit_API.messaging.enums.JobStatus;
import com.Orbit_API.messaging.enums.ProcessingStage;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.UUID;

@Component
public class ImageIngestMessageMapper {

    /**
     * Builds the RabbitMQ message DTO from a saved SatelliteImage and its upload request.
     * rawObjectPath must be the MinIO path where the raw file was already stored.
     */
    public ImageIngestMessageDTO toMessage(SatelliteImage image,
                                           UploadImageRequest request,
                                           String rawObjectPath,
                                           String rawBucket,
                                           String userId,
                                           String correlationId,
                                           int maxRetries) {
        ImageIngestMessageDTO msg = new ImageIngestMessageDTO();
        //msg.setJobId(UUID.randomUUID());
        msg.setImageId(image.getId());
        msg.setImageCode(image.getImageCode());
        msg.setUserId(userId);
        msg.setCorrelationId(correlationId);
        msg.setUploadMode(image.getUploadMode() != null ? image.getUploadMode() : "SINGLE_FILE_MODE");
        msg.setRawObjectPath(rawObjectPath);
        msg.setRawBucket(rawBucket);
        msg.setOriginalFileName(image.getImageCode()); // imageCode used as filename key
        msg.setTitle(request.getTitle());
        msg.setSatelliteName(request.getSatelliteName());
        msg.setSensorName(request.getSensorName());
        msg.setProcessingLevel(request.getProcessingLevel());
        msg.setAcquisitionDate(request.getAcquisitionDate());
        msg.setCloudCover(request.getCloudCover());
        msg.setResolutionM(request.getResolutionM());
        msg.setBandManifestJson(image.getBandManifestJson());
        msg.setSourceProductName(image.getSourceProductName());
        msg.setTileId(image.getTileId());
        msg.setRetryCount(0);
        msg.setMaxRetries(maxRetries);
        msg.setRequestedAt(LocalDateTime.now());
        return msg;
    }

    /**
     * Creates the ImageProcessingJob row to track this message lifecycle in DB.
     */
    public ImageProcessingJob toJob(ImageIngestMessageDTO msg,
                                    String queueName,
                                    String routingKey,
                                    String metadataJson) {
        ImageProcessingJob job = new ImageProcessingJob();
        job.setId(msg.getJobId());
        job.setImageId(msg.getImageId());
        job.setImageCode(msg.getImageCode());
        job.setJobType("IMAGE_INGEST");
        job.setQueueName(queueName);
        job.setRoutingKey(routingKey);
        job.setStatus(JobStatus.QUEUED);
        job.setStage(ProcessingStage.QUEUED_FOR_PROCESSING);
        job.setRetryCount(0);
        job.setMaxRetries(msg.getMaxRetries());
        job.setCorrelationId(msg.getCorrelationId());
        job.setRequestedBy(msg.getUserId());
        job.setRawObjectPath(msg.getRawObjectPath());
        job.setMetadataJson(metadataJson);
        return job;
    }
}


========================================================================================================================
FILE PATH: Orbit_API/messaging/publisher/ImageIngestPublisher.java
========================================================================================================================

package com.Orbit_API.messaging.publisher;

import com.Orbit_API.messaging.config.RabbitMQProperties;
import com.Orbit_API.messaging.dto.ImageIngestMessageDTO;
import com.Orbit_API.messaging.entity.ImageProcessingJob;
import com.Orbit_API.messaging.mapper.ImageIngestMessageMapper;
import com.Orbit_API.messaging.repository.ImageProcessingJobRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

/**
* Publishes an image ingest message to RabbitMQ.
*
* Called by ImageIngestOrchestrator after:
*   1. File validated
*   2. SatelliteImage row created (QUEUED)
*   3. Raw file uploaded to MinIO
*
* Publishes the job row first (within transaction), then sends to RabbitMQ.
* If RabbitMQ publish fails, the DB row stays QUEUED and can be retried by
* an outbox sweeper (optional future enhancement).
  */
  @Slf4j
  @Service
  public class ImageIngestPublisher {

  private final RabbitTemplate              rabbitTemplate;
  private final RabbitMQProperties          props;
  private final ImageProcessingJobRepository jobRepository;
  private final ImageIngestMessageMapper    mapper;
  private final ObjectMapper                objectMapper;

  public ImageIngestPublisher(RabbitTemplate rabbitTemplate,
  RabbitMQProperties props,
  ImageProcessingJobRepository jobRepository,
  ImageIngestMessageMapper mapper,
  ObjectMapper objectMapper) {
  this.rabbitTemplate = rabbitTemplate;
  this.props          = props;
  this.jobRepository  = jobRepository;
  this.mapper         = mapper;
  this.objectMapper   = objectMapper;
  }

  /**
    * Saves the ImageProcessingJob row and publishes the RabbitMQ message.
    * Both happen in the same Spring @Transactional scope so DB write is visible
    * before the AMQP message is sent.
    *
    * @param msg the fully-populated ingest message
      */
      //    @Transactional
      //    public void publish(ImageIngestMessageDTO msg) {
      //        String correlationId = msg.getCorrelationId();
      //        String imageCode     = msg.getImageCode();
      //
      //        // 1. Persist job row for tracking
      //        String metadataJson = serializeQuietly(msg);
      //        ImageProcessingJob job = mapper.toJob(msg,
      //                props.getIngestQueue(),
      //                props.getIngestRoutingKey(),
      //                metadataJson);
      //        jobRepository.save(job);
      //        log.info("[MQ-PUBLISH-JOB-SAVED] jobId={} imageCode={} correlationId={}",
      //                job.getId(), imageCode, correlationId);
      //
      //        // 2. Publish to RabbitMQ
      //        try {
      //            rabbitTemplate.convertAndSend(
      //                    props.getExchange(),
      //                    props.getIngestRoutingKey(),
      //                    msg
      //            );
      //            log.info("[MQ-PUBLISH-SUCCESS] exchange={} routingKey={} imageCode={} correlationId={}",
      //                    props.getExchange(), props.getIngestRoutingKey(), imageCode, correlationId);
      //        } catch (Exception ex) {
      //            log.error("[MQ-PUBLISH-FAILED] imageCode={} correlationId={} error={}",
      //                    imageCode, correlationId, ex.getMessage(), ex);
      //            // Job row is already saved as QUEUED — can be picked up by outbox sweeper later
      //            throw new RuntimeException("Failed to publish image ingest message to RabbitMQ: "
      //                    + ex.getMessage(), ex);
      //        }
      //    }




    @Transactional
    public void publish(ImageIngestMessageDTO msg) {
        String correlationId = msg.getCorrelationId();
        String imageCode     = msg.getImageCode();

        // 1. Persist job row FIRST (within this transaction)
        String metadataJson = serializeQuietly(msg);
        ImageProcessingJob job = mapper.toJob(msg, props.getIngestQueue(),
                props.getIngestRoutingKey(), metadataJson);
        ImageProcessingJob savedJob = jobRepository.save(job);
        msg.setJobId(savedJob.getId());   // ← sync the generated ID back to the message
        //msg.setJobId(savedJob.getId());   // sync generated ID back
        log.info("[MQ-PUBLISH-JOB-SAVED] jobId={} imageCode={} correlationId={}",
                savedJob.getId(), imageCode, correlationId);

        // 2. Send to RabbitMQ AFTER the DB transaction commits
        //    This prevents the consumer from seeing the job row before it exists
        final ImageIngestMessageDTO msgToSend = msg;
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                try {
                    rabbitTemplate.convertAndSend(
                            props.getExchange(),
                            props.getIngestRoutingKey(),
                            msgToSend
                    );
                    log.info("[MQ-PUBLISH-SENT] jobId={} imageCode={} correlationId={}",
                            msgToSend.getJobId(), imageCode, correlationId);
                } catch (Exception ex) {
                    log.error("[MQ-PUBLISH-FAILED] jobId={} error={}", msgToSend.getJobId(), ex.getMessage(), ex);
                    // Job row is QUEUED in DB — an outbox sweeper can retry this
                }
            }
        });
    }

    private String serializeQuietly(Object obj) {
        try {
            return objectMapper.writeValueAsString(obj);
        } catch (Exception ex) {
            log.warn("[MQ-PUBLISH] Could not serialize metadata for audit: {}", ex.getMessage());
            return "{}";
        }
    }
}

========================================================================================================================
FILE PATH: Orbit_API/messaging/repository/ImageProcessingJobRepository.java
========================================================================================================================

package com.Orbit_API.messaging.repository;



import com.Orbit_API.messaging.entity.ImageProcessingJob;
import com.Orbit_API.messaging.enums.JobStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ImageProcessingJobRepository extends JpaRepository<ImageProcessingJob, UUID> {

    Optional<ImageProcessingJob> findByImageId(UUID imageId);

    Optional<ImageProcessingJob> findByImageIdAndStatusNot(UUID imageId, JobStatus excluded);

    List<ImageProcessingJob> findByStatus(JobStatus status);

    List<ImageProcessingJob> findByCorrelationId(String correlationId);

    boolean existsByImageIdAndStatusIn(UUID imageId, List<JobStatus> statuses);

    /** Lightweight status update — avoids loading the full entity during status transitions. */
    @Modifying
    @Transactional
    @Query("UPDATE ImageProcessingJob j SET j.status = :status, j.updatedAt = CURRENT_TIMESTAMP WHERE j.id = :id")
    void updateStatus(@Param("id") UUID id, @Param("status") JobStatus status);
}

========================================================================================================================
FILE PATH: Orbit_API/messaging/service/ImageIngestOrchestrator.java
========================================================================================================================

package com.Orbit_API.messaging.service;



import com.Orbit_API.catalog.dto.UploadImageRequest;
import com.Orbit_API.catalog.dto.UploadImageResponseDTO;
import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.catalog.service.ImageValidationService;
import com.Orbit_API.exception.ImageProcessingException;
import com.Orbit_API.exception.ValidationException;
import com.Orbit_API.messaging.config.RabbitMQProperties;
import com.Orbit_API.messaging.dto.ImageIngestMessageDTO;
import com.Orbit_API.messaging.mapper.ImageIngestMessageMapper;
import com.Orbit_API.messaging.publisher.ImageIngestPublisher;
import com.Orbit_API.storage.MinioStorageService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.UUID;

/**
* Upload-side orchestrator for the RabbitMQ-based pipeline.
*
* Called by SatelliteImageController.upload() instead of the old AsyncImageProcessingService.
*
* SYNC steps (inside the HTTP request thread):
*   1. Validate file (extension, size, name)
*   2. Create SatelliteImage row with status QUEUED
*   3. Upload raw file to MinIO (raw/ prefix)
*   4. Build RabbitMQ message DTO
*   5. Publish message + create ImageProcessingJob row
*   6. Return UploadImageResponseDTO (202)
*
* All heavy processing is done by ImageIngestConsumer in a separate thread/process.
  */
  @Slf4j
  @Service
  public class ImageIngestOrchestrator {

  private final SatelliteImageRepository imageRepository;
  private final ImageValidationService   validationService;
  private final MinioStorageService      minioService;
  private final ImageIngestPublisher     publisher;
  private final ImageIngestMessageMapper mapper;
  private final RabbitMQProperties       mqProps;

  @Value("${app.upload.max-file-size:2147483648}")
  private long maxFileSize;

  @Value("${minio.bucket-raw}")
  private String rawBucket;

  public ImageIngestOrchestrator(SatelliteImageRepository imageRepository,
  ImageValidationService validationService,
  MinioStorageService minioService,
  ImageIngestPublisher publisher,
  ImageIngestMessageMapper mapper,
  RabbitMQProperties mqProps) {
  this.imageRepository   = imageRepository;
  this.validationService = validationService;
  this.minioService      = minioService;
  this.publisher         = publisher;
  this.mapper            = mapper;
  this.mqProps           = mqProps;
  }

  /**
    * Main entry point — called from SatelliteImageController.
    * Returns 202 Accepted immediately after publishing to RabbitMQ.
      */
      //@Transactional
      public UploadImageResponseDTO queueImageProcessing(MultipartFile file,
      UploadImageRequest request,
      String userId) {
      String correlationId = UUID.randomUUID().toString();
      log.info("[ORCHESTRATOR-START] correlationId={} user={} file={} size={}",
      correlationId, userId, file.getOriginalFilename(), file.getSize());

      // ── STEP 1: Validate ─────────────────────────────────────────────────
      validateFile(file);

      // ── STEP 2: Create QUEUED DB record ──────────────────────────────────
      SatelliteImage image = createQueuedRecord(file, request);
      log.info("[ORCHESTRATOR-REGISTERED] imageCode={} imageId={} correlationId={}",
      image.getImageCode(), image.getId(), correlationId);

      // ── STEP 3: Upload raw file to MinIO ──────────────────────────────────
      // File is uploaded to MinIO NOW so the consumer never touches the HTTP stream
      String rawObjectPath = uploadRawToMinio(file, image.getImageCode(), correlationId);
      image.setRawObjectPath(rawObjectPath);
      imageRepository.save(image);
      log.info("[ORCHESTRATOR-MINIO-RAW] path={} correlationId={}", rawObjectPath, correlationId);

      // ── STEP 4: Build RabbitMQ message ────────────────────────────────────
      ImageIngestMessageDTO msg = mapper.toMessage(
      image, request, rawObjectPath, rawBucket,
      userId, correlationId, mqProps.getMaxRetries());

      // ── STEP 5: Publish message + create job row ─────────────────────────
      publisher.publish(msg);
      log.info("[ORCHESTRATOR-QUEUED] jobId={} imageCode={} correlationId={}",
      msg.getJobId(), image.getImageCode(), correlationId);

      // ── STEP 6: Return 202 ───────────────────────────────────────────────
      return UploadImageResponseDTO.builder()
      .imageCode(image.getImageCode())
      .status(ImageProcessingStatus.PENDING.name())
      .trackingUrl("/api/v1/images/" + image.getId() + "/status")
      .message("Image queued for processing via RabbitMQ — correlationId: " + correlationId)
      .build();
      }

  // ── Private Helpers ──────────────────────────────────────────────────────

  private void validateFile(MultipartFile file) throws ValidationException {
  if (file == null || file.isEmpty()) {
  throw new ValidationException("File cannot be empty");
  }
  if (file.getSize() > maxFileSize) {
  throw new ValidationException(
  String.format("File size %d bytes exceeds maximum %d bytes", file.getSize(), maxFileSize));
  }
  if (file.getOriginalFilename() == null) {
  throw new ValidationException("File must have a name");
  }
  if (!validationService.isValidFileExtension(file.getOriginalFilename())) {
  throw new ValidationException(
  "Invalid file format. Allowed: .tif, .tiff, .jp2, .nitf, .ntf");
  }
  log.debug("[ORCHESTRATOR-VALIDATE-OK] {}", file.getOriginalFilename());
  }

  @Transactional
  private SatelliteImage createQueuedRecord(MultipartFile file, UploadImageRequest request) {
  SatelliteImage image = new SatelliteImage();
  image.setImageCode("IMG-" + UUID.randomUUID());
  // Use PENDING — existing ImageStatusService.getProgress() maps PENDING → 0%
  // Frontend sees no difference whether we call it PENDING or QUEUED
  image.setStatus(ImageProcessingStatus.PENDING.name());
  image.setTitle(request.getTitle());
  image.setSensorName(request.getSensorName());
  image.setSatelliteName(request.getSatelliteName());
  image.setProcessingLevel(request.getProcessingLevel());
  image.setAcquisitionDate(request.getAcquisitionDate());
  image.setCloudCover(request.getCloudCover());
  image.setResolutionM(request.getResolutionM());
  image.setCreatedAt(LocalDateTime.now());
  image.setUpdatedAt(LocalDateTime.now());
  return imageRepository.save(image);
  }

  private String uploadRawToMinio(MultipartFile file, String imageCode, String correlationId) {
  String objectPath = "raw/" + imageCode + "/" + file.getOriginalFilename();
  try (InputStream stream = file.getInputStream()) {
  minioService.upload(
  rawBucket,
  objectPath,
  stream,
  file.getSize(),
  file.getContentType() != null ? file.getContentType() : "application/octet-stream"
  );
  return objectPath;
  } catch (Exception ex) {
  log.error("[ORCHESTRATOR-MINIO-FAIL] correlationId={} error={}",
  correlationId, ex.getMessage(), ex);
  throw new ImageProcessingException(
  "Failed to upload raw file to MinIO: " + ex.getMessage(), ex);
  }
  }
  }


========================================================================================================================
FILE PATH: Orbit_API/processing/GdalProcessingService.java
========================================================================================================================

package com.Orbit_API.processing;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Polygon;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Path;

/**
* GDAL Processing Service
*
* Responsible for:
* - Running gdalinfo to extract metadata and footprints
* - Converting raster to Cloud Optimized GeoTIFF (COG)
* - Building polygon geometries for PostGIS storage
    */
    @Slf4j
    @Service
    public class GdalProcessingService {

private final ObjectMapper objectMapper = new ObjectMapper();

@Value("${gdal.path}")
private String gdalPath;

/**
    * Runs gdalinfo and returns the full JSON output as a Jackson tree.
    * Extracts: raster bounds, CRS, extent, geotransform, band info
    *
    * @param inputFile Path to satellite image file
    * @return JSON tree with GDAL metadata
    * @throws Exception if gdalinfo fails
      */
      public JsonNode runGdalInfoJson(Path inputFile) throws Exception {
      long startTime = System.currentTimeMillis();
      String absolutePath = inputFile.toAbsolutePath().toString();

      log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.info("║ [GDAL-GDALINFO-START] Executing gdalinfo                                      ║");
      log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.info("║ Input File     : {}", padRight(absolutePath, 63));
      log.info("║ File Size      : {} bytes", padRight(String.valueOf(inputFile.toFile().length()), 63));

      ProcessBuilder pb = new ProcessBuilder(
      gdalPath + "\\gdalinfo.exe",
      "-json",
      absolutePath
      );

      pb.redirectErrorStream(true); // merge stdout + stderr

      Process process = null;
      StringBuilder output = new StringBuilder();
      StringBuilder errorOutput = new StringBuilder();

      try {
      process = pb.start();
      log.debug("║ Process Started: {}", padRight("OK", 63));

           // Read stdout
           try (BufferedReader reader = new BufferedReader(
                   new InputStreamReader(process.getInputStream()))) {
               String line;
               while ((line = reader.readLine()) != null) {
                   output.append(line).append("\n");
               }
           }

           int exitCode = process.waitFor();
           long duration = System.currentTimeMillis() - startTime;

           log.info("║ Exit Code      : {}", padRight(String.valueOf(exitCode), 63));
           log.info("║ Output Size    : {} bytes", padRight(String.valueOf(output.length()), 63));
           log.info("║ Execution Time : {} ms", padRight(String.valueOf(duration), 63));

           if (exitCode != 0) {
               log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
               log.error("║ [GDAL-GDALINFO-FAILED] Exit code: {}", exitCode);
               log.error("║ GDALINFO Output (first 1000 chars):");
               log.error("║ {}", truncate(output.toString(), 1000));
               log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");
               
               throw new RuntimeException("gdalinfo failed. Exit code: " + exitCode);
           }

           JsonNode root = objectMapper.readTree(output.toString());
           
           log.info("║ Parsed JSON OK ✓");
           log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
           log.debug("║ GDAL JSON Fields: {}", root.fieldNames().toString());
           log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");

           return root;

      } catch (Exception ex) {
      long duration = System.currentTimeMillis() - startTime;
      log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.error("║ [GDAL-GDALINFO-ERROR] Exception occurred");
      log.error("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));
      log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));
      log.error("║ Execution Time : {} ms", padRight(String.valueOf(duration), 63));
      log.error("║ Stack Trace    :");
      log.error(ex.getMessage(), ex);
      log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");

           throw ex;
      }
      }

/**
    * Converts raster to Cloud Optimized GeoTIFF (COG)
    *
    * Compression: LZW
    * Overviews: Auto-generated
    * BigTIFF: Used when needed
    * Threading: All CPUs
    *
    * @param inputFile  Source raster file
    * @param outputFile Target COG file
    * @return Output file path
    * @throws Exception if conversion fails
      */
      public Path convertToCog(Path inputFile, Path outputFile) throws Exception {
      long startTime = System.currentTimeMillis();
      String inputPath = inputFile.toAbsolutePath().toString();
      String outputPath = outputFile.toAbsolutePath().toString();

      log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
      log.info("║ [GDAL-COG-CONVERT-START] Converting to Cloud Optimized GeoTIFF                ║");
      log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.info("║ Input  File    : {}", padRight(inputPath, 63));
      log.info("║ Output File    : {}", padRight(outputPath, 63));
      log.info("║ Compression    : LZW");
      log.info("║ BigTIFF        : IF_SAFER");
      log.info("║ Threads        : ALL_CPUS");

      ProcessBuilder pb = new ProcessBuilder(
      gdalPath + "\\gdal_translate.exe",
      inputPath,
      outputPath,
      "-of", "COG",
      "-co", "COMPRESS=LZW",
      "-co", "OVERVIEWS=IGNORE_EXISTING",
      "-co", "BIGTIFF=IF_SAFER",
      "-co", "NUM_THREADS=ALL_CPUS"
      );

      Process process = null;

      try {
      process = pb.start();
      log.debug("║ Process Started: OK");

           // Capture output (for debugging)
           StringBuilder output = new StringBuilder();
           try (BufferedReader reader = new BufferedReader(
                   new InputStreamReader(process.getInputStream()))) {
               String line;
               while ((line = reader.readLine()) != null) {
                   output.append(line).append("\n");
                   log.debug("║ GDAL Output: {}", line);
               }
           }

           int exitCode = process.waitFor();
           long duration = System.currentTimeMillis() - startTime;

           log.info("║ Exit Code      : {}", padRight(String.valueOf(exitCode), 63));
           log.info("║ Output Size    : {} bytes", padRight(String.valueOf(outputFile.toFile().length()), 63));
           log.info("║ Execution Time : {} ms", padRight(String.valueOf(duration), 63));

           if (exitCode != 0) {
               log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
               log.error("║ [GDAL-COG-CONVERT-FAILED] Exit code: {}", exitCode);
               log.error("║ GDAL Output: {}", output.toString());
               log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");
               
               throw new RuntimeException("COG conversion failed. Exit code: " + exitCode);
           }

           log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");
           return outputFile;

      } catch (Exception ex) {
      long duration = System.currentTimeMillis() - startTime;
      log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
      log.error("║ [GDAL-COG-CONVERT-ERROR] Exception occurred");
      log.error("║ Error Type     : {}", padRight(ex.getClass().getSimpleName(), 63));
      log.error("║ Error Message  : {}", padRight(ex.getMessage(), 63));
      log.error("║ Execution Time : {} ms", padRight(String.valueOf(duration), 63));
      log.error(ex.getMessage(), ex);
      log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");

           throw ex;
      }
      }

/**
    * Builds polygon footprint from GDAL's WGS84 extent
    * Coordinates are in EPSG:4326 (WGS84)
    *
    * @param root GDAL JSON metadata
    * @return JTS Polygon geometry
      */
      public Polygon buildFootprintFromGdalJson(JsonNode root) {
      log.info("[GDAL-FOOTPRINT-BUILD] Building polygon footprint from GDAL metadata");

      try {
      JsonNode extent = root.path("wgs84Extent");

           if (extent.isMissingNode()) {
               log.error("[GDAL-FOOTPRINT-ERROR] wgs84Extent not found in GDAL JSON");
               throw new IllegalArgumentException("wgs84Extent not found in GDAL JSON");
           }

           JsonNode coordinates = extent.path("coordinates");
           if (!coordinates.isArray() || coordinates.isEmpty()) {
               log.error("[GDAL-FOOTPRINT-ERROR] Invalid wgs84Extent.coordinates in GDAL JSON");
               throw new IllegalArgumentException("Invalid wgs84Extent.coordinates in GDAL JSON");
           }

           JsonNode ring = coordinates.get(0);
           if (!ring.isArray() || ring.size() < 4) {
               log.error("[GDAL-FOOTPRINT-ERROR] Invalid polygon ring in GDAL JSON");
               throw new IllegalArgumentException("Invalid polygon ring in GDAL JSON");
           }

           log.debug("[GDAL-FOOTPRINT-COORDS] Ring has {} coordinate points", ring.size());

           Coordinate[] coords = new Coordinate[ring.size()];
           for (int i = 0; i < ring.size(); i++) {
               JsonNode point = ring.get(i);
               double lon = point.get(0).asDouble();
               double lat = point.get(1).asDouble();
               coords[i] = new Coordinate(lon, lat);
           }

           GeometryFactory geometryFactory = new GeometryFactory();
           Polygon polygon = geometryFactory.createPolygon(coords);

           log.info("[GDAL-FOOTPRINT-SUCCESS] Polygon built with {} coordinates", coords.length);
           log.debug("[GDAL-FOOTPRINT-BOUNDS] Min X: {} Max X: {} Min Y: {} Max Y: {}",
                   polygon.getEnvelopeInternal().getMinX(),
                   polygon.getEnvelopeInternal().getMaxX(),
                   polygon.getEnvelopeInternal().getMinY(),
                   polygon.getEnvelopeInternal().getMaxY());

           return polygon;

      } catch (Exception ex) {
      log.error("[GDAL-FOOTPRINT-ERROR] Failed to build footprint", ex);
      throw new RuntimeException("Footprint building failed: " + ex.getMessage(), ex);
      }
      }

/**
    * Extracts the EPSG code from a gdalinfo JSON tree.
    *
    * Resolution order:
    *  1. coordinateSystem → id → code  (integer node, most reliable)
    *  2. coordinateSystem → proj4 string → parse "+zone=N" → derive UTM EPSG
    *  3. Default: 4326 (WGS84 geographic)
    *
    * @param gdalJson parsed gdalinfo -json output
    * @return EPSG integer code
      */
      public int extractEpsgCode(JsonNode gdalJson) {

      // --- Path 1: coordinateSystem.id.code (authoritative) ---
      JsonNode codeNode = gdalJson
      .path("coordinateSystem")
      .path("id")
      .path("code");

      if (!codeNode.isMissingNode() && codeNode.isNumber()) {
      int epsg = codeNode.asInt();
      log.info("[GDAL-CRS] EPSG extracted from coordinateSystem.id.code: {}", epsg);
      return epsg;
      }

      // --- Path 2: parse proj4 "+zone=N" → UTM EPSG ---
      JsonNode proj4Node = gdalJson
      .path("coordinateSystem")
      .path("proj4");

      if (!proj4Node.isMissingNode()) {
      String proj4 = proj4Node.asText();
      log.debug("[GDAL-CRS] id.code missing, attempting proj4 parse: {}", proj4);

           java.util.regex.Matcher zoneMatcher =
                   java.util.regex.Pattern.compile("\\+zone=(\\d+)")
                           .matcher(proj4);

           if (zoneMatcher.find()) {
               int zone = Integer.parseInt(zoneMatcher.group(1));

               // Determine hemisphere from "+south" flag
               boolean isSouthern = proj4.contains("+south");
               // Northern UTM: EPSG 32600 + zone  (e.g. zone 44 → 32644)
               // Southern UTM: EPSG 32700 + zone  (e.g. zone 44 → 32744)
               int epsg = (isSouthern ? 32700 : 32600) + zone;
               log.info("[GDAL-CRS] EPSG derived from proj4 +zone={} ({}): {}",
                       zone, isSouthern ? "south" : "north", epsg);
               return epsg;
           }
      }

      // --- Path 3: fallback ---
      log.warn("[GDAL-CRS] Could not extract EPSG from coordinateSystem — "
      + "neither id.code nor proj4 +zone found. Defaulting to EPSG:4326. "
      + "Image may have incorrect CRS stored.");
      return 4326;
      }

/**
    * Returns a text summary of GDAL metadata useful for debugging
    *
    * @param inputFile Path to satellite image
    * @return Pretty-printed JSON metadata
    * @throws Exception if metadata extraction fails
      */
      public String extractSummary(Path inputFile) throws Exception {
      log.info("[GDAL-SUMMARY] Extracting GDAL metadata summary");
      JsonNode root = runGdalInfoJson(inputFile);
      String summary = root.toPrettyString();
      log.debug("[GDAL-SUMMARY] Summary size: {} bytes", summary.length());
      return summary;
      }

// ===== HELPER METHODS =====

private String padRight(String s, int n) {
return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
}

private String truncate(String s, int maxLength) {
if (s.length() <= maxLength) return s;
return s.substring(0, maxLength) + "... (truncated)";
}
}

========================================================================================================================
FILE PATH: Orbit_API/processing/ImageMetadataService.java
========================================================================================================================

package com.Orbit_API.processing;

import com.Orbit_API.catalog.entity.SatelliteImage;
import com.fasterxml.jackson.databind.JsonNode;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Polygon;
import org.springframework.stereotype.Service;

import java.nio.file.Path;

@Slf4j
@Service
public class ImageMetadataService {

    private final GdalProcessingService gdalProcessingService;

    public ImageMetadataService(GdalProcessingService gdalProcessingService) {
        this.gdalProcessingService = gdalProcessingService;
    }

    /**
     * Minimal enrichment that is compatible with current SatelliteImage entity.
     * If you later add more fields to SatelliteImage (bounds, pixel size, etc.),
     * you can extend this method.
     */
    public void enrichMetadata(SatelliteImage image, String filePath) throws Exception {
        log.info("Enriching metadata for image: {}", image.getImageCode());

        try {
            JsonNode metadataJson = gdalProcessingService.runGdalInfoJson(Path.of(filePath));
            // Example: ensure CRS is set if not already
            if (image.getCrsEpsg() == null) {
                image.setCrsEpsg(4326);
            }
            // You can also reuse this JSON later if you add more fields
            log.info("Metadata JSON extracted for {} (keys: {})",
                    image.getImageCode(), metadataJson.fieldNames().toString());
        } catch (Exception ex) {
            log.error("Metadata enrichment failed: {}", ex.getMessage(), ex);
            throw ex;
        }
    }

    /**
     * Extract footprint geometry; currently returns WKT string, leaving it up
     * to the caller to convert/store if needed.
     */
    public String extractFootprint(String filePath) throws Exception {
        log.info("Extracting footprint from: {}", filePath);
        JsonNode root = gdalProcessingService.runGdalInfoJson(Path.of(filePath));
        Polygon polygon = gdalProcessingService.buildFootprintFromGdalJson(root);
        return polygon.toText(); // WKT
    }
}

========================================================================================================================
FILE PATH: Orbit_API/sentinel/controller/SentinelUploadController.java
========================================================================================================================

package com.Orbit_API.sentinel.controller;



import com.Orbit_API.exception.ValidationException;
import com.Orbit_API.sentinel.dto.SentinelUploadRequestDTO;
import com.Orbit_API.sentinel.dto.SentinelUploadResponseDTO;
import com.Orbit_API.sentinel.dto.SentinelValidationResponseDTO;
import com.Orbit_API.sentinel.service.SentinelBandValidationService;
import com.Orbit_API.sentinel.service.SentinelRgbIngestionService;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
* Sentinel-2 Upload Controller — completely separate from SatelliteImageController.
*
* Endpoints:
*   POST /api/v1/sentinel/validate  — dry-run band validation, no DB writes
*   POST /api/v1/sentinel/upload    — validate + ingest + async processing
    */
    @Slf4j
    @RestController
    @RequestMapping("/api/v1/sentinel")
    public class SentinelUploadController {

private final SentinelBandValidationService validationService;
private final SentinelRgbIngestionService   ingestionService;

public SentinelUploadController(SentinelBandValidationService validationService,
SentinelRgbIngestionService ingestionService) {
this.validationService = validationService;
this.ingestionService  = ingestionService;
}

/**
* POST /api/v1/sentinel/validate
* Dry-run validation — checks band filenames, completeness, tile/date consistency.
* Does NOT save anything to the database.
*
* Accept: multipart/form-data
*   bands: List<MultipartFile>  (B02, B03, B04 JP2/TIF files)
    */
    @PostMapping(value = "/validate", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<SentinelValidationResponseDTO> validate(
    @RequestPart("bands") List<MultipartFile> bands) {

     long start = System.currentTimeMillis();
     log.info("[SENTINEL-VALIDATE-REQUEST] files={}", bands.size());

     SentinelValidationResponseDTO result = validationService.validate(bands);
     long duration = System.currentTimeMillis() - start;

     log.info("[SENTINEL-VALIDATE-RESPONSE] valid={} errors={} in {}ms",
             result.isValid(), result.getErrors() == null ? 0 : result.getErrors().size(), duration);

     return ResponseEntity.ok(result);  // always 200 — validity is in the body
}

/**
* POST /api/v1/sentinel/upload
* Full Sentinel-2 RGB upload endpoint.
* Validates bands, creates DB record, queues async RGB pipeline.
* Returns 202 Accepted immediately.
*
* Accept: multipart/form-data
*   meta:  SentinelUploadRequestDTO (as JSON part)
*   bands: List<MultipartFile>      (B02, B03, B04 JP2/TIF files)
    */
    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<SentinelUploadResponseDTO> upload(
    @RequestPart("meta")  @Valid SentinelUploadRequestDTO request,
    @RequestPart("bands")        List<MultipartFile> bands) {

     long start = System.currentTimeMillis();
     log.info("[SENTINEL-UPLOAD-REQUEST] mode={} files={} title={}",
             request.getUploadMode(), bands.size(), request.getTitle());

     try {
         SentinelUploadResponseDTO response = ingestionService.submitBandUpload(request, bands);
         long duration = System.currentTimeMillis() - start;
         log.info("[SENTINEL-UPLOAD-ACCEPTED] imageCode={} in {}ms",
                 response.getImageCode(), duration);
         return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);  // 202

     } catch (ValidationException ex) {
         log.warn("[SENTINEL-UPLOAD-VALIDATION-FAILED] {}", ex.getMessage());
         return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
     } catch (Exception ex) {
         log.error("[SENTINEL-UPLOAD-ERROR] {}", ex.getMessage(), ex);
         return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
     }
}
}

========================================================================================================================
FILE PATH: Orbit_API/sentinel/dto/SentinelUploadRequestDTO.java
========================================================================================================================

package com.Orbit_API.sentinel.dto;



import com.Orbit_API.sentinel.enums.UploadMode;
import jakarta.validation.constraints.NotNull;

/**
* Metadata submitted alongside band files at POST /api/v1/sentinel/upload
* Band files are uploaded as separate @RequestPart multipart parts.
  */
  public class SentinelUploadRequestDTO {

  @NotNull(message = "Upload mode is required")
  private UploadMode uploadMode;

  private String title;
  private String satelliteName;   // e.g. "Sentinel-2"
  private String sensorName;      // e.g. "MSI"
  private String processingLevel; // e.g. "L2A"
  private Double cloudCover;
  private Double resolutionM;     // default 10.0 for Sentinel-2 RGB bands
  private String acquisitionDate; // ISO date string yyyy-MM-dd

  /**
    * Optional: product name from .SAFE package, e.g.
    * S2A_MSIL2A_20230601T053641_N0509_R005_T43RGP_20230601T091234
      */
      private String sourceProductName;

  /**
    * Optional tile ID extracted from filename, e.g. T43RGP
      */
      private String tileId;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public UploadMode getUploadMode()                       { return uploadMode; }
  public void setUploadMode(UploadMode m)                 { this.uploadMode = m; }
  public String getTitle()                                { return title; }
  public void setTitle(String t)                          { this.title = t; }
  public String getSatelliteName()                        { return satelliteName; }
  public void setSatelliteName(String s)                  { this.satelliteName = s; }
  public String getSensorName()                           { return sensorName; }
  public void setSensorName(String s)                     { this.sensorName = s; }
  public String getProcessingLevel()                      { return processingLevel; }
  public void setProcessingLevel(String p)                { this.processingLevel = p; }
  public Double getCloudCover()                           { return cloudCover; }
  public void setCloudCover(Double c)                     { this.cloudCover = c; }
  public Double getResolutionM()                          { return resolutionM; }
  public void setResolutionM(Double r)                    { this.resolutionM = r; }
  public String getAcquisitionDate()                      { return acquisitionDate; }
  public void setAcquisitionDate(String d)                { this.acquisitionDate = d; }
  public String getSourceProductName()                    { return sourceProductName; }
  public void setSourceProductName(String s)              { this.sourceProductName = s; }
  public String getTileId()                               { return tileId; }
  public void setTileId(String t)                         { this.tileId = t; }
  }


========================================================================================================================
FILE PATH: Orbit_API/sentinel/dto/SentinelUploadResponseDTO.java
========================================================================================================================

package com.Orbit_API.sentinel.dto;



import com.Orbit_API.sentinel.enums.UploadMode;

import java.util.UUID;

/**
* Returned 202 Accepted by POST /api/v1/sentinel/upload
  */
  public class SentinelUploadResponseDTO {

  private UUID imageId;
  private String imageCode;
  private String status;          // PENDING → PROCESSING → ... → PUBLISHED
  private UploadMode uploadMode;
  private String trackingUrl;     // GET /api/v1/images/{id}/status
  private String previewPngPath;  // null until processing complete
  private String previewJpegPath; // null until processing complete
  private String message;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public UUID getImageId()                                { return imageId; }
  public void setImageId(UUID id)                         { this.imageId = id; }
  public String getImageCode()                            { return imageCode; }
  public void setImageCode(String c)                      { this.imageCode = c; }
  public String getStatus()                               { return status; }
  public void setStatus(String s)                         { this.status = s; }
  public UploadMode getUploadMode()                       { return uploadMode; }
  public void setUploadMode(UploadMode m)                 { this.uploadMode = m; }
  public String getTrackingUrl()                          { return trackingUrl; }
  public void setTrackingUrl(String u)                    { this.trackingUrl = u; }
  public String getPreviewPngPath()                       { return previewPngPath; }
  public void setPreviewPngPath(String p)                 { this.previewPngPath = p; }
  public String getPreviewJpegPath()                      { return previewJpegPath; }
  public void setPreviewJpegPath(String p)                { this.previewJpegPath = p; }
  public String getMessage()                              { return message; }
  public void setMessage(String m)                        { this.message = m; }
  }


========================================================================================================================
FILE PATH: Orbit_API/sentinel/dto/SentinelValidationResponseDTO.java
========================================================================================================================

package com.Orbit_API.sentinel.dto;


import java.util.List;

/**
* Returned by POST /api/v1/sentinel/validate — dry-run band validation result.
  */
  public class SentinelValidationResponseDTO {

  private boolean valid;
  private String detectedTileId;
  private String detectedProductName;
  private String detectedAcquisitionDate;
  private List<String> detectedBands;
  private List<String> errors;
  private List<String> warnings;
  private String message;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public boolean isValid()                                { return valid; }
  public void setValid(boolean v)                         { this.valid = v; }
  public String getDetectedTileId()                       { return detectedTileId; }
  public void setDetectedTileId(String t)                 { this.detectedTileId = t; }
  public String getDetectedProductName()                  { return detectedProductName; }
  public void setDetectedProductName(String p)            { this.detectedProductName = p; }
  public String getDetectedAcquisitionDate()              { return detectedAcquisitionDate; }
  public void setDetectedAcquisitionDate(String d)        { this.detectedAcquisitionDate = d; }
  public List<String> getDetectedBands()                  { return detectedBands; }
  public void setDetectedBands(List<String> b)            { this.detectedBands = b; }
  public List<String> getErrors()                         { return errors; }
  public void setErrors(List<String> e)                   { this.errors = e; }
  public List<String> getWarnings()                       { return warnings; }
  public void setWarnings(List<String> w)                 { this.warnings = w; }
  public String getMessage()                              { return message; }
  public void setMessage(String m)                        { this.message = m; }
  }


========================================================================================================================
FILE PATH: Orbit_API/sentinel/entity/SentinelBandManifest.java
========================================================================================================================

package com.Orbit_API.sentinel.entity;


import java.util.Map;

/**
* In-memory value object representing a validated set of Sentinel-2 band files.
* Not persisted as a DB table — serialized as JSON and stored in SatelliteImage.bandManifestJson.
  */
  public class SentinelBandManifest {

  private String tileId;              // e.g. T43RGP
  private String productName;         // e.g. S2A_MSIL2A_20230601T053641_...
  private String acquisitionDate;     // e.g. 20230601
  private String processingLevel;     // e.g. L2A

  /**
    * Map of bandId → local temp file path
    * e.g. { "B02" -> "/tmp/.../B02.jp2", "B03" -> "...", "B04" -> "..." }
      */
      private Map<String, String> bandPaths;

  // ── Getters & Setters ───────────────────────────────────────────────────
  public String getTileId()                               { return tileId; }
  public void setTileId(String t)                         { this.tileId = t; }
  public String getProductName()                          { return productName; }
  public void setProductName(String p)                    { this.productName = p; }
  public String getAcquisitionDate()                      { return acquisitionDate; }
  public void setAcquisitionDate(String d)                { this.acquisitionDate = d; }
  public String getProcessingLevel()                      { return processingLevel; }
  public void setProcessingLevel(String p)                { this.processingLevel = p; }
  public Map<String, String> getBandPaths()               { return bandPaths; }
  public void setBandPaths(Map<String, String> b)         { this.bandPaths = b; }
  }

========================================================================================================================
FILE PATH: Orbit_API/sentinel/enums/BandGroupType.java
========================================================================================================================

package com.Orbit_API.sentinel.enums;

public enum BandGroupType {
RGB_TRUE_COLOR,     // B02, B03, B04 — true color composite
ANALYTICAL,         // B08, B11, B12 — false color / NDVI
FULL_RGB_ANALYTICAL // B02–B04 + B08/B11/B12 — combined
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/enums/ExportMode.java
========================================================================================================================

package com.Orbit_API.sentinel.enums;



public enum ExportMode {
SINGLE_IMAGE,   // one full-extent PNG or JPEG
TILED_ZIP,      // many patch tiles zipped
AOI_CROP        // AOI-clipped single output
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/enums/UploadMode.java
========================================================================================================================

package com.Orbit_API.sentinel.enums;

public enum UploadMode {
SINGLE_FILE_MODE,       // existing GeoTIFF/JP2/NITF — handled by existing pipeline
SENTINEL_RGB_MODE,      // B02 + B03 + B04 uploaded as separate files
SAFE_PACKAGE_MODE,      // .SAFE zip uploaded — bands extracted internally
FUTURE_ANALYTICAL_MODE  // B08/B11/B12 for NDVI/SWIR — reserved for future
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/processing/SentinelGdalService.java
========================================================================================================================

package com.Orbit_API.sentinel.processing;


import com.Orbit_API.exception.ImageProcessingException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
* All GDAL operations for Sentinel-2 RGB ingestion.
*
* Pipeline:
*   1. buildVrt()        → gdalbuildvrt (stacks B04/B03/B02 into a virtual VRT)
*   2. scaleTo8bit()     → gdal_translate -scale (12-bit reflectance → 8-bit display)
*   3. convertToCog()    → gdal_translate -co TILED=YES -co COMPRESS=DEFLATE
*   4. toPng()           → gdal_translate -of PNG
*   5. toJpeg()          → gdal_translate -of JPEG -co QUALITY=90
*
* WHY SCALING IS MANDATORY:
*   Sentinel-2 JP2 stores reflectance * 10000 (12-bit range 0–10000).
*   PNG/JPEG is 8-bit (0–255). Without -scale 0 3000 0 255 all pixels
*   appear black because the raw values are far above 255 — gdal_translate
*   clips them all to max 255 which saturates bright areas, or to 0 which
*   makes dark areas invisible. The -scale option performs a linear stretch
*   mapping typical surface reflectance (0–3000) to display range (0–255).
    */
    @Slf4j
    @Service
    public class SentinelGdalService {

@Value("${gdal.path}")
private String gdalPath;

@Value("${gdal.sentinel.scale-min:0}")
private int scaleMin;

@Value("${gdal.sentinel.scale-max:3000}")
private int scaleMax;

/**
* Step 1 — Build a multi-band VRT stacking bands in R-G-B order.
*
* GDAL command:
*   gdalbuildvrt -separate rgb.vrt B04.jp2 B03.jp2 B02.jp2
*
* @param bandPaths ordered map: {"B04" → path, "B03" → path, "B02" → path}
* @param outputDir working directory
* @param correlationId for logging
* @return path to generated .vrt file
  */
  public Path buildVrt(Map<String, Path> bandPaths, Path outputDir, String correlationId) {
  log.info("[SENTINEL-VRT-START] correlationId={}", correlationId);

  Path vrtOutput = outputDir.resolve("rgb_stack.vrt");

  List<String> cmd = new ArrayList<>();
  cmd.add(gdalPath + "/gdalbuildvrt");
  cmd.add("-separate");           // each input file = one band in VRT
  cmd.add(vrtOutput.toAbsolutePath().toString());

  // ORDER MATTERS: B04=Red, B03=Green, B02=Blue
  for (String band : new String[]{"B04", "B03", "B02"}) {
  Path p = bandPaths.get(band);
  if (p == null) {
  throw new ImageProcessingException("Missing band " + band + " for VRT construction");
  }
  cmd.add(p.toAbsolutePath().toString());
  }

  runCommand(cmd, "GDAL-BUILDVRT", correlationId);
  log.info("[SENTINEL-VRT-SUCCESS] VRT created: {}", vrtOutput);
  return vrtOutput;
  }

/**
* Step 2 — Scale 12-bit reflectance values to 8-bit for visual clarity.
*
* GDAL command:
*   gdal_translate -scale 0 3000 0 255 -exponent 0.5 \
*                  -ot Byte -of GTiff \
*                  rgb_stack.vrt rgb_scaled.tif
*
* The -exponent 0.5 applies a gamma correction (sqrt) which brightens
* the midtones, producing a more natural-looking image than pure linear stretch.
*
* @param vrtInput   path to the VRT from buildVrt()
* @param outputDir  working directory
* @param correlationId for logging
* @return path to scaled 8-bit GeoTIFF
  */
  public Path scaleTo8bit(Path vrtInput, Path outputDir, String correlationId) {
  log.info("[SENTINEL-SCALE-START] correlationId={} scaleMin={} scaleMax={}",
  correlationId, scaleMin, scaleMax);

  Path scaledOutput = outputDir.resolve("rgb_scaled.tif");

  List<String> cmd = List.of(
  gdalPath + "/gdal_translate",
  "-scale", String.valueOf(scaleMin), String.valueOf(scaleMax), "0", "255",
  "-exponent", "0.5",         // gamma correction — brightens midtones
  "-ot",       "Byte",        // output data type: 8-bit unsigned
  "-of",       "GTiff",
  "-co",       "PHOTOMETRIC=RGB",
  vrtInput.toAbsolutePath().toString(),
  scaledOutput.toAbsolutePath().toString()
  );

  runCommand(cmd, "GDAL-SCALE", correlationId);
  log.info("[SENTINEL-SCALE-SUCCESS] Scaled 8-bit RGB: {}", scaledOutput);
  return scaledOutput;
  }

/**
* Step 3 — Convert scaled GeoTIFF to Cloud Optimized GeoTIFF (COG).
*
* GDAL command:
*   gdal_translate -of COG \
*                  -co COMPRESS=DEFLATE \
*                  -co TILED=YES \
*                  -co OVERVIEW_RESAMPLING=AVERAGE \
*                  rgb_scaled.tif rgb_cog.tif
*/
public Path convertToCog(Path scaledInput, Path outputDir, String correlationId) {
log.info("[SENTINEL-COG-START] correlationId={}", correlationId);

     Path cogOutput = outputDir.resolve("rgb_cog.tif");

     List<String> cmd = List.of(
             gdalPath + "/gdal_translate",
             "-of",  "COG",
             "-co",  "COMPRESS=DEFLATE",
             "-co",  "TILED=YES",
             "-co",  "OVERVIEW_RESAMPLING=AVERAGE",
             scaledInput.toAbsolutePath().toString(),
             cogOutput.toAbsolutePath().toString()
     );

     runCommand(cmd, "GDAL-COG", correlationId);
     log.info("[SENTINEL-COG-SUCCESS] COG created: {}", cogOutput);
     return cogOutput;
}

/**
* Step 4 — Generate full-extent PNG preview.
*
* GDAL command:
*   gdal_translate -of PNG rgb_scaled.tif preview.png
*
* Note: input must already be 8-bit (from scaleTo8bit step).
  */
  public Path toPng(Path scaledInput, Path outputDir, String correlationId) {
  log.info("[SENTINEL-PNG-START] correlationId={}", correlationId);

  Path pngOutput = outputDir.resolve("preview.png");

  List<String> cmd = List.of(
  gdalPath + "/gdal_translate",
  "-of", "PNG",
  scaledInput.toAbsolutePath().toString(),
  pngOutput.toAbsolutePath().toString()
  );

  runCommand(cmd, "GDAL-PNG", correlationId);
  log.info("[SENTINEL-PNG-SUCCESS] PNG created: {}", pngOutput);
  return pngOutput;
  }

/**
* Step 5 — Generate full-extent JPEG preview.
*
* GDAL command:
*   gdal_translate -of JPEG -co QUALITY=90 rgb_scaled.tif preview.jpg
    */
    public Path toJpeg(Path scaledInput, Path outputDir, String correlationId) {
    log.info("[SENTINEL-JPEG-START] correlationId={}", correlationId);

     Path jpegOutput = outputDir.resolve("preview.jpg");

     List<String> cmd = List.of(
             gdalPath + "/gdal_translate",
             "-of", "JPEG",
             "-co", "QUALITY=90",
             scaledInput.toAbsolutePath().toString(),
             jpegOutput.toAbsolutePath().toString()
     );

     runCommand(cmd, "GDAL-JPEG", correlationId);
     log.info("[SENTINEL-JPEG-SUCCESS] JPEG created: {}", jpegOutput);
     return jpegOutput;
}

// ── Private Helpers ──────────────────────────────────────────────────────

private void runCommand(List<String> cmd, String label, String correlationId) {
try {
log.debug("[{}] correlationId={} cmd={}", label, correlationId, String.join(" ", cmd));
ProcessBuilder pb = new ProcessBuilder(cmd);
pb.redirectErrorStream(true);
Process process   = pb.start();

         StringBuilder output = new StringBuilder();
         try (BufferedReader reader = new BufferedReader(
                 new InputStreamReader(process.getInputStream()))) {
             String line;
             while ((line = reader.readLine()) != null) {
                 output.append(line).append("\n");
                 log.debug("[{}-OUT] {}", label, line);
             }
         }

         int exitCode = process.waitFor();
         if (exitCode != 0) {
             log.error("[{}-FAILED] correlationId={} exitCode={} output={}",
                     label, correlationId, exitCode, output);
             throw new ImageProcessingException(label + " failed with exit code "
                     + exitCode + ": " + output.toString().substring(
                     0, Math.min(300, output.length())));
         }
     } catch (ImageProcessingException ex) {
         throw ex;
     } catch (Exception ex) {
         throw new ImageProcessingException(label + " process error: " + ex.getMessage(), ex);
     }
}
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/service/SentinelBandValidationService.java
========================================================================================================================

package com.Orbit_API.sentinel.service;


import com.Orbit_API.sentinel.dto.SentinelValidationResponseDTO;
import com.Orbit_API.sentinel.entity.SentinelBandManifest;
import org.springframework.web.multipart.MultipartFile;
import com.Orbit_API.exception.ValidationException;

import java.util.List;

public interface SentinelBandValidationService {

    /**
     * Full dry-run validation — does NOT save anything.
     * Returns a report with detected metadata and any errors.
     */
    SentinelValidationResponseDTO validate(List<MultipartFile> bandFiles);

    /**
     * Validates band files and returns a resolved manifest for processing.
     * Throws ValidationException if any check fails.
     */
    SentinelBandManifest validateAndBuildManifest(List<MultipartFile> bandFiles);
}

========================================================================================================================
FILE PATH: Orbit_API/sentinel/service/SentinelRgbIngestionService.java
========================================================================================================================

package com.Orbit_API.sentinel.service;



import com.Orbit_API.sentinel.dto.SentinelUploadRequestDTO;
import com.Orbit_API.sentinel.dto.SentinelUploadResponseDTO;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface SentinelRgbIngestionService {

    /**
     * Validates bands, creates a PENDING DB record, queues async RGB processing.
     * Returns 202 immediately.
     */
    SentinelUploadResponseDTO submitBandUpload(SentinelUploadRequestDTO request,
                                               List<MultipartFile> bandFiles);
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/service/impl/SentinelBandValidationServiceImpl.java
========================================================================================================================

package com.Orbit_API.sentinel.service.impl;



import com.Orbit_API.exception.ValidationException;
import com.Orbit_API.sentinel.dto.SentinelValidationResponseDTO;
import com.Orbit_API.sentinel.entity.SentinelBandManifest;
import com.Orbit_API.sentinel.service.SentinelBandValidationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
* Production-grade validator for Sentinel-2 multi-band uploads.
*
* Sentinel-2 band filename patterns supported:
*   ESA standard: T43RGP_20230601T053641_B02_10m.jp2
*   Short:        B02.jp2 / B02.tif
*   SAFE product: S2A_MSIL2A_20230601T053641_N0509_R005_T43RGP_20230601T091234_B02_10m.jp2
    */
    @Slf4j
    @Service
    public class SentinelBandValidationServiceImpl implements SentinelBandValidationService {

/**
* Full ESA Sentinel-2 band filename:
* group 1 = tileId   (e.g. T43RGP)
* group 2 = date     (e.g. 20230601)
* group 3 = bandId   (e.g. B02)
* group 4 = resolution (optional, e.g. 10m)
* group 5 = extension (.jp2 or .tif)
  */
  private static final Pattern ESA_BAND_PATTERN = Pattern.compile(
  "(?:.*_)?(T[0-9]{2}[A-Z]{3})_(\\d{8})T\\d{6}_?(B\\d{2})(?:_\\d+m)?\\.(jp2|tif|tiff)",
  Pattern.CASE_INSENSITIVE
  );

/** Short band filename: B02.jp2 or B03.tif */
private static final Pattern SHORT_BAND_PATTERN = Pattern.compile(
"(B\\d{2})\\.(jp2|tif|tiff)",
Pattern.CASE_INSENSITIVE
);

private static final Set<String> RGB_REQUIRED_BANDS    = Set.of("B02", "B03", "B04");
private static final Set<String> ALLOWED_EXTENSIONS    = Set.of(".jp2", ".tif", ".tiff");
private static final long        MAX_BAND_SIZE_BYTES   = 500L * 1024 * 1024; // 500 MB per band

@Override
public SentinelValidationResponseDTO validate(List<MultipartFile> bandFiles) {
SentinelValidationResponseDTO response = new SentinelValidationResponseDTO();
List<String> errors   = new ArrayList<>();
List<String> warnings = new ArrayList<>();

     if (bandFiles == null || bandFiles.isEmpty()) {
         response.setValid(false);
         response.setErrors(List.of("No band files provided"));
         response.setMessage("Validation failed: no files uploaded");
         return response;
     }

     try {
         SentinelBandManifest manifest = internalValidate(bandFiles, errors, warnings);
         boolean valid = errors.isEmpty();

         response.setValid(valid);
         response.setErrors(errors);
         response.setWarnings(warnings);

         if (manifest != null) {
             response.setDetectedTileId(manifest.getTileId());
             response.setDetectedProductName(manifest.getProductName());
             response.setDetectedAcquisitionDate(manifest.getAcquisitionDate());
             response.setDetectedBands(new ArrayList<>(manifest.getBandPaths().keySet()));
         }

         response.setMessage(valid
                 ? "All " + bandFiles.size() + " band files passed validation"
                 : errors.size() + " validation error(s) found");

     } catch (Exception ex) {
         response.setValid(false);
         response.setErrors(List.of("Internal validation error: " + ex.getMessage()));
         response.setMessage("Validation failed with unexpected error");
     }

     return response;
}

@Override
public SentinelBandManifest validateAndBuildManifest(List<MultipartFile> bandFiles)
throws ValidationException {

     List<String> errors   = new ArrayList<>();
     List<String> warnings = new ArrayList<>();

     SentinelBandManifest manifest = internalValidate(bandFiles, errors, warnings);

     if (!errors.isEmpty()) {
         String combined = String.join("; ", errors);
         log.warn("[SENTINEL-VALIDATE-FAIL] {} error(s): {}", errors.size(), combined);
         throw new ValidationException("Sentinel-2 band validation failed: " + combined);
     }

     if (!warnings.isEmpty()) {
         warnings.forEach(w -> log.warn("[SENTINEL-VALIDATE-WARN] {}", w));
     }

     return manifest;
}

// ── Core Validation Logic ────────────────────────────────────────────────

private SentinelBandManifest internalValidate(List<MultipartFile> bandFiles,
List<String> errors,
List<String> warnings) {
Map<String, String>  bandIdToFilename = new LinkedHashMap<>();
Map<String, String>  bandIdToTileId   = new LinkedHashMap<>();
Map<String, String>  bandIdToDate     = new LinkedHashMap<>();

     for (MultipartFile file : bandFiles) {
         String filename = file.getOriginalFilename();
         if (filename == null || filename.isBlank()) {
             errors.add("One or more files have no filename");
             continue;
         }

         // 1. Extension check
         String lower = filename.toLowerCase();
         boolean validExt = ALLOWED_EXTENSIONS.stream().anyMatch(lower::endsWith);
         if (!validExt) {
             errors.add("File '" + filename + "' has unsupported extension. Allowed: .jp2, .tif, .tiff");
             continue;
         }

         // 2. File size check
         if (file.getSize() > MAX_BAND_SIZE_BYTES) {
             errors.add("File '" + filename + "' exceeds 500 MB limit (" + (file.getSize() / 1024 / 1024) + " MB)");
             continue;
         }

         if (file.getSize() == 0) {
             errors.add("File '" + filename + "' is empty");
             continue;
         }

         // 3. Band ID extraction — try ESA pattern first, then short pattern
         String bandId   = null;
         String tileId   = null;
         String dateStr  = null;

         Matcher esaMatcher = ESA_BAND_PATTERN.matcher(filename);
         if (esaMatcher.matches()) {
             tileId  = esaMatcher.group(1).toUpperCase();
             dateStr = esaMatcher.group(2);
             bandId  = esaMatcher.group(3).toUpperCase();
             log.debug("[SENTINEL-VALIDATE] ESA pattern matched: file={} tile={} date={} band={}",
                     filename, tileId, dateStr, bandId);
         } else {
             Matcher shortMatcher = SHORT_BAND_PATTERN.matcher(filename);
             if (shortMatcher.matches()) {
                 bandId = shortMatcher.group(1).toUpperCase();
                 log.debug("[SENTINEL-VALIDATE] Short pattern matched: file={} band={}", filename, bandId);
                 warnings.add("File '" + filename + "' uses short naming — tile/date cannot be cross-validated");
             } else {
                 errors.add("File '" + filename + "' does not match any known Sentinel-2 band naming pattern");
                 continue;
             }
         }

         // 4. Duplicate band check
         if (bandIdToFilename.containsKey(bandId)) {
             errors.add("Duplicate band '" + bandId + "': files '"
                     + bandIdToFilename.get(bandId) + "' and '" + filename + "'");
             continue;
         }

         bandIdToFilename.put(bandId, filename);
         if (tileId  != null) bandIdToTileId.put(bandId, tileId);
         if (dateStr != null) bandIdToDate.put(bandId, dateStr);
     }

     // 5. Cross-band tile consistency — all must have the same tile ID
     Set<String> distinctTiles = new HashSet<>(bandIdToTileId.values());
     if (distinctTiles.size() > 1) {
         errors.add("Band files belong to different tiles: " + distinctTiles
                 + " — all bands must be from the same Sentinel-2 tile");
     }

     // 6. Cross-band date consistency
     Set<String> distinctDates = new HashSet<>(bandIdToDate.values());
     if (distinctDates.size() > 1) {
         errors.add("Band files have different acquisition dates: " + distinctDates
                 + " — mixing bands from different dates is not allowed");
     }

     // 7. RGB completeness check
     Set<String> uploadedBands = bandIdToFilename.keySet();
     List<String> missingRgb   = new ArrayList<>();
     for (String required : RGB_REQUIRED_BANDS) {
         if (!uploadedBands.contains(required)) missingRgb.add(required);
     }
     if (!missingRgb.isEmpty()) {
         errors.add("Missing required RGB bands: " + missingRgb
                 + ". Required: B02 (Blue), B03 (Green), B04 (Red)");
     }

     if (!errors.isEmpty()) {
         return null; // no manifest if validation failed
     }

     // Build manifest
     SentinelBandManifest manifest = new SentinelBandManifest();
     manifest.setTileId(!bandIdToTileId.isEmpty()
             ? bandIdToTileId.values().iterator().next() : "UNKNOWN");
     manifest.setAcquisitionDate(!bandIdToDate.isEmpty()
             ? bandIdToDate.values().iterator().next() : "UNKNOWN");
     manifest.setBandPaths(new LinkedHashMap<>(bandIdToFilename)); // stores filenames here, paths filled later
     log.info("[SENTINEL-VALIDATE-OK] tileId={} date={} bands={}",
             manifest.getTileId(), manifest.getAcquisitionDate(), uploadedBands);
     return manifest;
}
}


========================================================================================================================
FILE PATH: Orbit_API/sentinel/service/impl/SentinelRgbIngestionServiceImpl.java
========================================================================================================================

package com.Orbit_API.sentinel.service.impl;



import com.Orbit_API.catalog.entity.ImageProcessingStatus;
import com.Orbit_API.catalog.entity.SatelliteImage;
import com.Orbit_API.catalog.repository.SatelliteImageRepository;
import com.Orbit_API.exception.ValidationException;
import com.Orbit_API.processing.GdalProcessingService;
import com.Orbit_API.sentinel.dto.SentinelUploadRequestDTO;
import com.Orbit_API.sentinel.dto.SentinelUploadResponseDTO;
import com.Orbit_API.sentinel.entity.SentinelBandManifest;
import com.Orbit_API.sentinel.enums.UploadMode;
import com.Orbit_API.sentinel.processing.SentinelGdalService;
import com.Orbit_API.sentinel.service.SentinelBandValidationService;
import com.Orbit_API.sentinel.service.SentinelRgbIngestionService;
import com.Orbit_API.storage.MinioStorageService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Polygon;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.file.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

/**
* Orchestrates the full Sentinel-2 RGB ingestion pipeline.
*
* Sync (immediate):
*   validate → save temp files → create PENDING DB record → return 202
*
* Async (background):
*   buildVrt → scaleTo8bit → toCog → toPng → toJpeg
*   → upload all to MinIO → update DB status → cleanup temp
    */
    @Slf4j
    @Service
    public class SentinelRgbIngestionServiceImpl implements SentinelRgbIngestionService {

private final SentinelBandValidationService validationService;
private final SentinelGdalService           gdalSentinelService;
private final GdalProcessingService         gdalProcessingService;
private final MinioStorageService           minioStorageService;
private final SatelliteImageRepository      imageRepository;
private final ObjectMapper                  objectMapper;

@Value("${minio.bucket-raw}")
private String rawBucket;

@Value("${minio.bucket-cog}")
private String cogBucket;

@Value("${minio.bucket-previews:orbitview-previews}")
private String previewBucket;

@Value("${app.upload.temp-dir:/tmp/orbitview}")
private String tempDir;

@Value("${orbitview.shared-data-dir}")
private String sharedDataDir;

public SentinelRgbIngestionServiceImpl(
SentinelBandValidationService validationService,
SentinelGdalService gdalSentinelService,
GdalProcessingService gdalProcessingService,
MinioStorageService minioStorageService,
SatelliteImageRepository imageRepository,
ObjectMapper objectMapper) {
this.validationService    = validationService;
this.gdalSentinelService  = gdalSentinelService;
this.gdalProcessingService = gdalProcessingService;
this.minioStorageService  = minioStorageService;
this.imageRepository      = imageRepository;
this.objectMapper         = objectMapper;
}

// ── A. SYNC: Validate + Register ────────────────────────────────────────

@Override
@Transactional
public SentinelUploadResponseDTO submitBandUpload(SentinelUploadRequestDTO request,
List<MultipartFile> bandFiles) {
String correlationId = UUID.randomUUID().toString();
log.info("[SENTINEL-SUBMIT-START] correlationId={} mode={} files={}",
correlationId, request.getUploadMode(), bandFiles.size());

     // 1. Validate bands — throws ValidationException on failure
     SentinelBandManifest manifest = validationService.validateAndBuildManifest(bandFiles);
     log.info("[SENTINEL-SUBMIT-VALIDATED] tileId={} date={} bands={}",
             manifest.getTileId(), manifest.getAcquisitionDate(),
             manifest.getBandPaths().keySet());

     // 2. Save band files to temp disk
     String imageCode = "SENT-" + UUID.randomUUID();
     Path   workDir;
     Map<String, Path> savedBandPaths = new LinkedHashMap<>();
     try {
         workDir = Files.createDirectories(Path.of(tempDir, "sentinel", imageCode));
         for (MultipartFile file : bandFiles) {
             String fname   = Objects.requireNonNull(file.getOriginalFilename());
             String bandId  = extractBandId(fname);
             Path   dest    = workDir.resolve(bandId + getExtension(fname));
             file.transferTo(dest);
             savedBandPaths.put(bandId, dest);
             log.debug("[SENTINEL-SUBMIT] Saved band {} → {}", bandId, dest);
         }
     } catch (Exception ex) {
         throw new RuntimeException("Failed to save temp band files: " + ex.getMessage(), ex);
     }

     // Update manifest with actual temp paths
     Map<String, String> pathMap = new LinkedHashMap<>();
     savedBandPaths.forEach((k, v) -> pathMap.put(k, v.toAbsolutePath().toString()));
     manifest.setBandPaths(pathMap);

     // 3. Create PENDING DB record
     SatelliteImage image = new SatelliteImage();
     image.setImageCode(imageCode);
     image.setStatus(ImageProcessingStatus.PENDING.name());
     image.setUploadMode(UploadMode.SENTINEL_RGB_MODE.name());
     image.setTitle(request.getTitle() != null
             ? request.getTitle() : "Sentinel-2 " + manifest.getTileId());
     image.setSatelliteName(request.getSatelliteName() != null
             ? request.getSatelliteName() : "Sentinel-2");
     image.setSensorName(request.getSensorName() != null
             ? request.getSensorName() : "MSI");
     image.setProcessingLevel(request.getProcessingLevel() != null
             ? request.getProcessingLevel() : manifest.getProcessingLevel());
     image.setTileId(manifest.getTileId());
     image.setSourceProductName(manifest.getProductName());

     if (request.getAcquisitionDate() != null) {
         try { image.setAcquisitionDate(LocalDate.parse(request.getAcquisitionDate())); }
         catch (Exception e) { log.warn("[SENTINEL-SUBMIT] Could not parse acquisitionDate"); }
     }
     if (request.getCloudCover()  != null) image.setCloudCover(request.getCloudCover());
     if (request.getResolutionM() != null) image.setResolutionM(request.getResolutionM());
     else image.setResolutionM(10.0); // Sentinel-2 RGB bands default to 10m

     // Store manifest as JSON for audit/reprocessing
     try {
         image.setBandManifestJson(objectMapper.writeValueAsString(manifest));
     } catch (Exception e) {
         log.warn("[SENTINEL-SUBMIT] Could not serialize band manifest");
     }

     image.setCreatedAt(LocalDateTime.now());
     image.setUpdatedAt(LocalDateTime.now());
     SatelliteImage saved = imageRepository.save(image);

     log.info("[SENTINEL-SUBMIT-REGISTERED] imageCode={} id={}", imageCode, saved.getId());

     // 4. Trigger async pipeline
     runSentinelPipelineAsync(saved.getId(), savedBandPaths, correlationId);

     // 5. Return 202
     SentinelUploadResponseDTO response = new SentinelUploadResponseDTO();
     response.setImageId(saved.getId());
     response.setImageCode(imageCode);
     response.setStatus(ImageProcessingStatus.PENDING.name());
     response.setUploadMode(UploadMode.SENTINEL_RGB_MODE);
     response.setTrackingUrl("/api/v1/images/" + saved.getId() + "/status");
     response.setMessage("Sentinel-2 bands validated and queued for RGB processing");
     return response;
}

// ── B. ASYNC: Full RGB Pipeline ──────────────────────────────────────────

@Async("imageProcessingExecutor")
public void runSentinelPipelineAsync(UUID imageId,
Map<String, Path> bandPaths,
String correlationId) {
log.info("[SENTINEL-PIPELINE-START] imageId={} correlationId={}", imageId, correlationId);

     Path workDir = bandPaths.values().iterator().next().getParent();

     try {
         SatelliteImage image = imageRepository.findById(imageId)
                 .orElseThrow(() -> new RuntimeException("Image not found: " + imageId));

         // Mark PROCESSING
         image.setStatus(ImageProcessingStatus.PROCESSING.name());
         imageRepository.save(image);

         // STEP 1 — Build VRT (B04=R, B03=G, B02=B)
         log.info("[SENTINEL-STEP-1/7] Building RGB VRT stack");
         Path vrtFile = gdalSentinelService.buildVrt(bandPaths, workDir, correlationId);

         // STEP 2 — Scale 12-bit → 8-bit with gamma correction
         // This is the critical step that prevents black output
         log.info("[SENTINEL-STEP-2/7] Scaling 12-bit reflectance to 8-bit display range");
         Path scaledTif = gdalSentinelService.scaleTo8bit(vrtFile, workDir, correlationId);

         // STEP 3 — Convert scaled TIF to COG
         log.info("[SENTINEL-STEP-3/7] Converting to Cloud Optimized GeoTIFF");
         Path cogFile = gdalSentinelService.convertToCog(scaledTif, workDir, correlationId);

         // STEP 4 — Extract footprint and CRS from COG via existing GdalProcessingService
         log.info("[SENTINEL-STEP-4/7] Extracting footprint and CRS via gdalinfo");
         com.fasterxml.jackson.databind.JsonNode gdalJson =
                 gdalProcessingService.runGdalInfoJson(cogFile);
         Polygon footprint = gdalProcessingService.buildFootprintFromGdalJson(gdalJson);
         int epsgCode      = gdalProcessingService.extractEpsgCode(gdalJson);
         image.setFootprint(footprint);
         image.setCrsEpsg(epsgCode);

         // STEP 5 — Generate PNG and JPEG previews
         log.info("[SENTINEL-STEP-5/7] Generating PNG and JPEG previews");
         Path pngFile  = gdalSentinelService.toPng(scaledTif, workDir, correlationId);
         Path jpegFile = gdalSentinelService.toJpeg(scaledTif, workDir, correlationId);

         // STEP 6 — Upload all outputs to MinIO
         log.info("[SENTINEL-STEP-6/7] Uploading outputs to MinIO");
         String imageCode = image.getImageCode();

         // Upload raw band files as a bundle
         for (Map.Entry<String, Path> entry : bandPaths.entrySet()) {
             String rawPath = "raw/" + imageCode + "/" + entry.getKey() + ".jp2";
             minioStorageService.uploadFile(rawBucket, rawPath, entry.getValue());
             if (image.getRawObjectPath() == null) image.setRawObjectPath(rawPath);
         }

         // Upload COG
         String cogPath = "cog/" + imageCode + "/rgb_cog.tif";
         minioStorageService.uploadFile(cogBucket, cogPath, cogFile);
         image.setCogObjectPath(cogPath);

         // Upload PNG preview
         String pngPath = "previews/" + imageCode + "/preview.png";
         minioStorageService.uploadFile(previewBucket, pngPath, pngFile);
         image.setPreviewPngPath(pngPath);

         // Upload JPEG preview
         String jpegPath = "previews/" + imageCode + "/preview.jpg";
         minioStorageService.uploadFile(previewBucket, jpegPath, jpegFile);
         image.setPreviewJpegPath(jpegPath);

         // STEP 7 — Copy COG to GeoServer shared dir and mark complete
         log.info("[SENTINEL-STEP-7/7] Copying COG to GeoServer shared directory");
         Path sharedCogDir  = Files.createDirectories(
                 Path.of(sharedDataDir, "cogs", imageCode));
         Path sharedCogFile = sharedCogDir.resolve("processed.tif");
         Files.copy(cogFile, sharedCogFile, StandardCopyOption.REPLACE_EXISTING);

         image.setStatus(ImageProcessingStatus.PROCESSING_COMPLETE.name());
         imageRepository.save(image);

         log.info("[SENTINEL-PIPELINE-SUCCESS] imageCode={} correlationId={} epsg={} pngPath={} jpegPath={}",
                 imageCode, correlationId, epsgCode, pngPath, jpegPath);

     } catch (Exception ex) {
         log.error("[SENTINEL-PIPELINE-FAILED] imageId={} correlationId={} error={}",
                 imageId, correlationId, ex.getMessage(), ex);
         try {
             SatelliteImage image = imageRepository.findById(imageId).orElse(null);
             if (image != null) {
                 image.setStatus(ImageProcessingStatus.FAILED.name());
                 imageRepository.save(image);
             }
         } catch (Exception saveEx) {
             log.error("[SENTINEL-PIPELINE-SAVE-ERROR] {}", saveEx.getMessage());
         }
     } finally {
         cleanupDir(workDir);
     }
}

// ── Private Helpers ──────────────────────────────────────────────────────

private String extractBandId(String filename) {
// Try ESA pattern first
java.util.regex.Matcher m = java.util.regex.Pattern
.compile("(?:.*_)?(B\\d{2})(?:_\\d+m)?\\.(jp2|tif|tiff)",
java.util.regex.Pattern.CASE_INSENSITIVE)
.matcher(filename);
if (m.matches()) return m.group(1).toUpperCase();
// Short pattern: B02.jp2
m = java.util.regex.Pattern
.compile("(B\\d{2})\\.(jp2|tif|tiff)",
java.util.regex.Pattern.CASE_INSENSITIVE)
.matcher(filename);
if (m.matches()) return m.group(1).toUpperCase();
return filename.replace(".", "_"); // fallback
}

private String getExtension(String filename) {
int dot = filename.lastIndexOf('.');
return dot >= 0 ? filename.substring(dot) : ".jp2";
}

private void cleanupDir(Path dir) {
if (dir == null) return;
try (var walk = Files.walk(dir)) {
walk.sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(File::delete);
log.debug("[SENTINEL-CLEANUP] Removed temp dir: {}", dir);
} catch (Exception ex) {
log.warn("[SENTINEL-CLEANUP-WARN] {}", ex.getMessage());
}
}
}


========================================================================================================================
FILE PATH: Orbit_API/storage/MinioRetryService.java
========================================================================================================================

package com.Orbit_API.storage;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.nio.file.Path;

@Slf4j
@Service
public class MinioRetryService {

    private final MinioStorageService minioStorageService;

    @Value("${minio.upload.retry-attempts:3}")
    private int maxRetries;

    public MinioRetryService(MinioStorageService minioStorageService) {
        this.minioStorageService = minioStorageService;
    }

    public String uploadWithRetry(String bucket, String objectName, Path file, String fileType) throws Exception {
        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                log.info("MinIO upload attempt {}/{}: {}/{}", attempt, maxRetries, bucket, objectName);
                return minioStorageService.uploadFile(bucket, objectName, file);
            } catch (Exception ex) {
                log.warn("MinIO upload attempt {} failed: {}", attempt, ex.getMessage());

                if (attempt < maxRetries) {
                    // Exponential backoff
                    long delayMs = (long) Math.pow(2, attempt) * 1000;
                    log.info("Retrying after {} ms", delayMs);
                    Thread.sleep(delayMs);
                } else {
                    throw new Exception("MinIO upload failed after " + maxRetries + " attempts", ex);
                }
            }
        }
        throw new Exception("MinIO upload failed");
    }
}

========================================================================================================================
FILE PATH: Orbit_API/storage/MinioStorageService.java
========================================================================================================================

package com.Orbit_API.storage;

import io.minio.*;
import io.minio.http.Method;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import jakarta.annotation.PostConstruct;
import java.util.List;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;

/**
* MinIO Storage Service
*
* Responsible for:
* - Ensuring bucket existence
* - Uploading files (raw images, COGs, thumbnails)
* - Creating signed download URLs
* - Deleting objects
    */
    @Slf4j
    @Service
    public class MinioStorageService {

private final MinioClient minioClient;

@Value("${minio.bucket-raw}")
private String rawBucket;

@Value("${minio.bucket-cog}")
private String cogBucket;

@Value("${minio.bucket-thumb}")
private String thumbBucket;

@Value("${minio.bucket-exports}")
private String exportBucket;

public MinioStorageService(MinioClient minioClient) {
this.minioClient = minioClient;
log.info("[MINIO-INIT] MinioStorageService initialized");
}

/**
    * Runs ONCE at Spring startup — ensures all required MinIO buckets exist.
    * If any bucket cannot be verified or created, the application will FAIL TO START
    * because processing is impossible without storage.
      */
      @PostConstruct
      public void ensureBuckets() {
      log.info("");
      log.info("╔══════════════════════════════════════════════════════════════════╗");
      log.info("║       MINIO-BUCKETS-CHECK  Verifying MinIO buckets              ║");
      log.info("╚══════════════════════════════════════════════════════════════════╝");

      try {
      //            for (String bucket : List.of(rawBucket, cogBucket, thumbBucket)) {
      //                createBucketIfMissing(bucket);
      //            }
      for (String bucket : List.of(
      rawBucket,
      cogBucket,
      thumbBucket,
      exportBucket
      )) {
      createBucketIfMissing(bucket);
      }
      log.info("[MINIO-BUCKETS-READY] All buckets verified successfully");

      } catch (Exception ex) {
      log.error("");
      log.error("[MINIO-BUCKETS-FATAL] Cannot start OrbitView — bucket setup failed");
      log.error("  Error : {}", ex.getMessage());
      log.error(ex.getMessage(), ex);
      log.error("");
      throw new RuntimeException(
      "MinIO bucket initialization failed — application cannot start: " + ex.getMessage(), ex
      );
      }
      }


    /**
     * Creates a single bucket if it does not already exist.
     * @param bucket Bucket name
     * @throws Exception if MinIO operation fails
     */
    private void createBucketIfMissing(String bucket) throws Exception {
        try {
            boolean exists = minioClient.bucketExists(
                    BucketExistsArgs.builder().bucket(bucket).build()
            );
            if (!exists) {
                log.info("[MINIO-BUCKET-CREATE] Creating bucket: {}", bucket);
                minioClient.makeBucket(
                        MakeBucketArgs.builder().bucket(bucket).build()
                );
                log.info("[MINIO-BUCKET-CREATE-SUCCESS] Bucket created: {}", bucket);
            } else {
                log.info("[MINIO-BUCKET-EXISTS] Bucket already exists: {}", bucket);
            }
        } catch (Exception ex) {
            log.error("[MINIO-BUCKET-ERROR] Failed to check/create bucket: {}", bucket);
            throw ex;  // re-thrown to ensureBuckets() which wraps as RuntimeException
        }
    }

//    /**
//     * Creates bucket if it doesn't exist
//     *
//     * @param bucket Bucket name
//     * @throws Exception if operation fails
//     */
//    private void createBucketIfMissing(String bucket) throws Exception {
//        try {
//            boolean exists = minioClient.bucketExists(
//                    BucketExistsArgs.builder().bucket(bucket).build()
//            );
//
//            if (!exists) {
//                log.info("[MINIO-BUCKET-CREATE] Creating bucket: {}", bucket);
//                minioClient.makeBucket(
//                        MakeBucketArgs.builder().bucket(bucket).build()
//                );
//                log.info("[MINIO-BUCKET-CREATE-SUCCESS] Bucket created: {}", bucket);
//            } else {
//                log.debug("[MINIO-BUCKET-EXISTS] Bucket already exists: {}", bucket);
//            }
//        } catch (Exception ex) {
//            log.error("[MINIO-BUCKET-ERROR] Failed to check/create bucket: {}", bucket, ex);
//            throw ex;
//        }
//    }

    /**
     * Uploads a file stream into MinIO
     * 
     * @param bucket      Target bucket
     * @param objectName  Object path in bucket
     * @param stream      Input stream
     * @param size        Stream size in bytes
     * @param contentType MIME type
     * @return Object path
     * @throws Exception if upload fails
     */
    public String upload(String bucket, String objectName, InputStream stream, long size, String contentType) throws Exception {
        long startTime = System.currentTimeMillis();
        
        log.info("╔═══════════════════════════════════════════════════════════════════════════════╗");
        log.info("║ [MINIO-UPLOAD-START] Uploading file to MinIO                                 ║");
        log.info("╠═══════════════════════════════════════════════════════════════════════════════╣");
        log.info("║ Bucket         : {}", padRight(bucket, 63));
        log.info("║ Object Path    : {}", padRight(objectName, 63));
        log.info("║ Size           : {} bytes ({} MB)", size, (size / 1024 / 1024));
        log.info("║ Content Type   : {}", padRight(contentType, 63));

        try {
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucket)
                            .object(objectName)
                            .stream(stream, size, -1)
                            .contentType(contentType)
                            .build()
            );
            
            long duration = System.currentTimeMillis() - startTime;
            log.info("║ Upload Status  : SUCCESS ✓");
            log.info("║ Execution Time : {} ms", duration);
            log.info("╚═══════════════════════════════════════════════════════════════════════════════╝");
            
            return objectName;
            
        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("╠═══════════════════════════════════════════════════════════════════════════════╣");
            log.error("║ [MINIO-UPLOAD-FAILED] Upload failed");
            log.error("║ Bucket         : {}", bucket);
            log.error("║ Object Path    : {}", objectName);
            log.error("║ Error Type     : {}", ex.getClass().getSimpleName());
            log.error("║ Error Message  : {}", ex.getMessage());
            log.error("║ Execution Time : {} ms", duration);
            log.error(ex.getMessage(), ex);
            log.error("╚═══════════════════════════════════════════════════════════════════════════════╝");
            
            throw ex;
        }
    }

    /**
     * Uploads a file from filesystem to MinIO
     * 
     * @param bucket     Target bucket
     * @param objectName Object path in bucket
     * @param file       File path
     * @return Object path
     * @throws Exception if upload fails
     */
    public String uploadFile(String bucket, String objectName, Path file) throws Exception {
        long startTime = System.currentTimeMillis();
        long fileSize = Files.size(file);
        String contentType = Files.probeContentType(file);
        
        if (contentType == null) {
            contentType = "application/octet-stream";
        }

        log.info("[MINIO-UPLOAD-FILE] Uploading file from filesystem");
        log.debug("║ Local File     : {}", file.toAbsolutePath());
        log.debug("║ File Size      : {} bytes", fileSize);
        
        try (InputStream inputStream = Files.newInputStream(file)) {
            String result = upload(bucket, objectName, inputStream, fileSize, contentType);
            
            long duration = System.currentTimeMillis() - startTime;
            log.info("[MINIO-UPLOAD-FILE-SUCCESS] File uploaded successfully");
            log.debug("║ Duration       : {} ms", duration);
            
            return result;
        }
    }

    /**
     * Creates a temporary signed URL for secure download
     * URL expires after specified minutes
     * 
     * @param bucket         Source bucket
     * @param objectName     Object path
     * @param expiryMinutes  URL expiry time in minutes
     * @return Signed URL string
     * @throws Exception if URL generation fails
     */
    public String createSignedDownloadUrl(String bucket, String objectName, int expiryMinutes) throws Exception {
        long startTime = System.currentTimeMillis();
        
        log.info("[MINIO-SIGNED-URL-CREATE] Generating signed download URL");
        log.debug("║ Bucket         : {}", bucket);
        log.debug("║ Object         : {}", objectName);
        log.debug("║ Expiry         : {} minutes", expiryMinutes);
        
        try {
            String url = minioClient.getPresignedObjectUrl(
                    GetPresignedObjectUrlArgs.builder()
                            .method(Method.GET)
                            .bucket(bucket)
                            .object(objectName)
                            .expiry(expiryMinutes, TimeUnit.MINUTES)
                            .build()
            );
            
            long duration = System.currentTimeMillis() - startTime;
            log.info("[MINIO-SIGNED-URL-SUCCESS] Signed URL generated");
            log.debug("║ URL Length     : {} chars", url.length());
            log.debug("║ Duration       : {} ms", duration);
            
            return url;
            
        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[MINIO-SIGNED-URL-ERROR] Failed to generate signed URL", ex);
            log.error("║ Bucket         : {}", bucket);
            log.error("║ Object         : {}", objectName);
            log.error("║ Error Message  : {}", ex.getMessage());
            log.error("║ Duration       : {} ms", duration);
            
            throw ex;
        }
    }

    /**
     * Deletes object from MinIO
     * 
     * @param bucket     Source bucket
     * @param objectPath Object path
     */
    public void deleteObject(String bucket, String objectPath) {
        long startTime = System.currentTimeMillis();
        
        log.info("[MINIO-DELETE-START] Deleting object from MinIO");
        log.debug("║ Bucket         : {}", bucket);
        log.debug("║ Object Path    : {}", objectPath);
        
        try {
            minioClient.removeObject(
                    RemoveObjectArgs.builder()
                            .bucket(bucket)
                            .object(objectPath)
                            .build()
            );
            
            long duration = System.currentTimeMillis() - startTime;
            log.info("[MINIO-DELETE-SUCCESS] Object deleted successfully");
            log.debug("║ Duration       : {} ms", duration);
            
        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[MINIO-DELETE-FAILED] Failed to delete MinIO object", ex);
            log.error("║ Bucket         : {}", bucket);
            log.error("║ Object Path    : {}", objectPath);
            log.error("║ Error Message  : {}", ex.getMessage());
            log.error("║ Duration       : {} ms", duration);
            
            throw new RuntimeException("MinIO delete failed: " + ex.getMessage(), ex);
        }
    }

    /**
     * Downloads an object from MinIO and returns it as an InputStream.
     * Caller MUST close the stream after use (use try-with-resources).
     *
     * @param bucket     Source bucket
     * @param objectPath Object path in bucket
     * @return InputStream of the object content
     * @throws Exception if download fails
     */
    public InputStream downloadObject(String bucket, String objectPath) throws Exception {
        long startTime = System.currentTimeMillis();

        log.info("[MINIO-DOWNLOAD-START] bucket={} path={}", bucket, objectPath);

        try {
            InputStream stream = minioClient.getObject(
                    GetObjectArgs.builder()
                            .bucket(bucket)
                            .object(objectPath)
                            .build()
            );

            long duration = System.currentTimeMillis() - startTime;
            log.info("[MINIO-DOWNLOAD-OK] bucket={} path={} in {}ms", bucket, objectPath, duration);

            return stream;

        } catch (Exception ex) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("[MINIO-DOWNLOAD-FAILED] bucket={} path={} error={} in {}ms",
                    bucket, objectPath, ex.getMessage(), duration);
            throw ex;
        }
    }

    // ===== HELPER METHODS =====
    private String padRight(String s, int n) {
        return String.format("%-" + n + "s", s).substring(0, Math.min(s.length(), n));
    }
}

========================================================================================================================
FILE PATH: Orbit_API/users/User.java
========================================================================================================================

package com.Orbit_API.users;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String username;

    @Column(nullable = false, unique = true)
    private String email;

    private String role;

    private LocalDateTime createdAt = LocalDateTime.now();
    
    

	public User() {
		super();
	}

	public User(Long id, String username, String email, String role, LocalDateTime createdAt) {
		super();
		this.id = id;
		this.username = username;
		this.email = email;
		this.role = role;
		this.createdAt = createdAt;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getRole() {
		return role;
	}

	public void setRole(String role) {
		this.role = role;
	}

	public LocalDateTime getCreatedAt() {
		return createdAt;
	}

	public void setCreatedAt(LocalDateTime createdAt) {
		this.createdAt = createdAt;
	}






}


========================================================================================================================
FILE PATH: Orbit_API/users/UserRepository.java
========================================================================================================================

package com.Orbit_API.users;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
}

========================================================================================================================
FILE PATH: Orbit_API/util/GeoJsonUtil.java
========================================================================================================================

package com.Orbit_API.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.LinearRing;
import org.locationtech.jts.geom.Polygon;
import org.locationtech.jts.geom.PrecisionModel;
import org.locationtech.jts.io.geojson.GeoJsonWriter;
import org.springframework.stereotype.Component;

/**
* GeoJsonUtil — Static helpers for GeoJSON ↔ JTS Polygon conversion.
*
* Method 1: polygonToGeoJson(Polygon)     — JTS → GeoJSON geometry string
* Method 2: geoJsonStringToPolygon(String) — GeoJSON string → JTS Polygon (SRID 4326)
*
* All coordinates follow GeoJSON standard: [longitude, latitude] order.
  */
  @Slf4j
  @Component
  public class GeoJsonUtil {

  private static final int                WGS84_SRID      = 4326;
  private static final ObjectMapper       OBJECT_MAPPER   = new ObjectMapper();

  // GeometryFactory pre-configured with SRID 4326 (WGS84)
  private static final GeometryFactory    GEOMETRY_FACTORY =
  new GeometryFactory(new PrecisionModel(), WGS84_SRID);

  // Private constructor — utility class, no instantiation needed
  private GeoJsonUtil() {}

  // ═════════════════════════════════════════════════════════════════════════
  // Method 1 — polygonToGeoJson : JTS Polygon → GeoJSON geometry string
  // ═════════════════════════════════════════════════════════════════════════

  /**
    * Converts a JTS Polygon to a GeoJSON geometry string.
    *
    * Output format:
    * {"type":"Polygon","coordinates":[[[lon,lat],[lon,lat],...,[lon,lat]]]}
    *
    * @param polygon JTS Polygon (may be null)
    * @return GeoJSON geometry string, or null if input is null
      */
      public static String polygonToGeoJson(Polygon polygon) {
      if (polygon == null) {
      log.debug("[GeoJsonUtil] polygonToGeoJson — input is null, returning null");
      return null;
      }

      try {
      GeoJsonWriter writer = new GeoJsonWriter();
      // Disable encoding CRS in output — frontend expects plain geometry, not a CRS block
      writer.setEncodeCRS(false);
      String geoJson = writer.write(polygon);
      log.debug("[GeoJsonUtil] polygonToGeoJson — converted polygon with {} coordinates",
      polygon.getNumPoints());
      return geoJson;

      } catch (Exception ex) {
      log.error("[GeoJsonUtil] polygonToGeoJson — conversion failed: {}", ex.getMessage(), ex);
      throw new IllegalStateException("Failed to convert JTS Polygon to GeoJSON: " + ex.getMessage(), ex);
      }
      }

  // ═════════════════════════════════════════════════════════════════════════
  // Method 2 — geoJsonStringToPolygon : GeoJSON string → JTS Polygon
  // ═════════════════════════════════════════════════════════════════════════

  /**
    * Parses a GeoJSON Polygon geometry string into a JTS Polygon with SRID 4326.
    *
    * Handles both formats:
    *   Format A — full geometry object:
    *     {"type":"Polygon","coordinates":[[[77.0,28.4],[77.5,28.4],...,[77.0,28.4]]]}
    *   Format B — raw coordinates array only:
    *     [[[77.0,28.4],[77.5,28.4],...,[77.0,28.4]]]
    *
    * GeoJSON ring rules enforced:
    *   - Minimum 4 coordinate pairs (first and last must be identical to close the ring)
    *   - Coordinates must be [longitude, latitude] (GeoJSON standard)
    *
    * @param geoJsonPolygon GeoJSON string from OpenLayers frontend
    * @return JTS Polygon with SRID set to 4326
    * @throws IllegalArgumentException if input is null, blank, or has fewer than 4 coordinate points
      */
      public static Polygon geoJsonStringToPolygon(String geoJsonPolygon) {
      // ── Input validation ──────────────────────────────────────────────────
      if (geoJsonPolygon == null || geoJsonPolygon.isBlank()) {
      throw new IllegalArgumentException(
      "GeoJSON polygon string must not be null or empty");
      }

      try {
      JsonNode root = OBJECT_MAPPER.readTree(geoJsonPolygon.trim());
      JsonNode coordinatesNode;

           // ── Detect input format ───────────────────────────────────────────
           if (root.isObject()) {
               // Format A: {"type":"Polygon","coordinates":[...]}
               String type = root.path("type").asText("");
               if (!type.equals("Polygon")) {
                   throw new IllegalArgumentException(
                           "GeoJSON type must be 'Polygon', found: '" + type + "'");
               }
               coordinatesNode = root.path("coordinates");
               if (coordinatesNode.isMissingNode()) {
                   throw new IllegalArgumentException(
                           "GeoJSON Polygon object is missing the 'coordinates' field");
               }
           } else if (root.isArray()) {
               // Format B: [[[lon,lat],...]] — raw coordinates array
               coordinatesNode = root;
               log.debug("[GeoJsonUtil] geoJsonStringToPolygon — detected raw coordinates array format");
           } else {
               throw new IllegalArgumentException(
                       "Unrecognized GeoJSON format — must be a Polygon object or coordinates array");
           }

           // ── Extract outer ring (first ring of coordinates) ─────────────────
           // GeoJSON Polygon: coordinates[0] = exterior ring, coordinates[1+] = holes (ignored here)
           JsonNode outerRingNode = coordinatesNode.get(0);
           if (outerRingNode == null || !outerRingNode.isArray()) {
               throw new IllegalArgumentException(
                       "GeoJSON Polygon must contain at least one coordinate ring");
           }

           int numPoints = outerRingNode.size();
           if (numPoints < 4) {
               throw new IllegalArgumentException(
                       "GeoJSON Polygon ring must have at least 4 coordinate points (got " + numPoints
                               + "). A valid polygon needs minimum 3 unique vertices + closing point.");
           }

           // ── Build JTS Coordinate array ─────────────────────────────────────
           Coordinate[] coordinates = new Coordinate[numPoints];
           for (int i = 0; i < numPoints; i++) {
               JsonNode point = outerRingNode.get(i);
               if (point == null || !point.isArray() || point.size() < 2) {
                   throw new IllegalArgumentException(
                           "Invalid coordinate at index " + i
                                   + ": expected [longitude, latitude] array");
               }
               double longitude = point.get(0).asDouble();   // GeoJSON: first value is longitude (X)
               double latitude  = point.get(1).asDouble();   // GeoJSON: second value is latitude (Y)
               coordinates[i]   = new Coordinate(longitude, latitude);
           }

           // ── Ensure the ring is closed (first == last coordinate) ───────────
           // GeoJSON requires first and last to be identical; JTS LinearRing also requires this.
           if (!coordinates[0].equals2D(coordinates[numPoints - 1])) {
               log.debug("[GeoJsonUtil] geoJsonStringToPolygon — ring not closed, auto-closing");
               Coordinate[] closed = new Coordinate[numPoints + 1];
               System.arraycopy(coordinates, 0, closed, 0, numPoints);
               closed[numPoints] = new Coordinate(coordinates[0]);
               coordinates = closed;
           }

           // ── Create JTS LinearRing and Polygon ──────────────────────────────
           LinearRing shell   = GEOMETRY_FACTORY.createLinearRing(coordinates);
           Polygon    polygon = GEOMETRY_FACTORY.createPolygon(shell, null); // null = no holes

           // ── Set SRID 4326 explicitly ───────────────────────────────────────
           // GeometryFactory already embeds SRID, but setSRID ensures it is present
           // on the geometry object itself (required for Hibernate Spatial / PostGIS).
           polygon.setSRID(WGS84_SRID);

           log.debug("[GeoJsonUtil] geoJsonStringToPolygon — built polygon with {} points, SRID={}",
                   polygon.getNumPoints(), polygon.getSRID());

           return polygon;

      } catch (IllegalArgumentException ex) {
      // Re-throw as-is — these are intentional validation failures
      throw ex;
      } catch (Exception ex) {
      log.error("[GeoJsonUtil] geoJsonStringToPolygon — failed to parse GeoJSON: {}", ex.getMessage(), ex);
      throw new IllegalArgumentException(
      "Failed to parse GeoJSON polygon string: " + ex.getMessage(), ex);
      }
      }
      }






---

### Resource Files

#### src/main/resources/application.yml
# ===== gdal (Keycloak OAuth2) =====

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║           ORBITVIEW APPLICATION CONFIGURATION (COMPLETE)                   ║
# ║  With RabbitMQ Message Queue, PostgreSQL, MinIO, GeoServer, Keycloak      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════════════════════
# GDAL CONFIGURATION (Image Processing)
# ═══════════════════════════════════════════════════════════════════════════════

gdal:
path: C:/OSGeo4W/bin                  # Windows: C:/OSGeo4W/bin
# Linux: /usr/bin or /usr/local/bin
sentinel:
scale-min: 0                        # Min reflectance value for Sentinel-2
scale-max: 3000                     # Max reflectance value for Sentinel-2


# ═══════════════════════════════════════════════════════════════════════════════
# CORS CONFIGURATION (Legacy - prefer spring.web.cors below)
# ═══════════════════════════════════════════════════════════════════════════════

cors:
# Development default — override in production/staging
# Multiple origins: https://app.example.com,https://admin.example.com
allowed-origins: http://localhost:3000


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

server:
port: 8089                            # API server port
servlet:
context-path: /                     # Root context path
compression:
enabled: true                       # Enable gzip compression
min-response-size: 1024             # Compress responses > 1KB
shutdown: graceful                    # Graceful shutdown
tomcat:
max-http-post-size: 5368709120      # 5GB max POST size


# ═══════════════════════════════════════════════════════════════════════════════
# SPRING FRAMEWORK CORE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

spring:
application:
name: OrbitView-Satellite-Portal    # Application name
version: 1.0.0                      # Application version

# ─────────────────────────────────────────────────────────────────────────
# DATASOURCE (PostgreSQL + PostGIS)
# ─────────────────────────────────────────────────────────────────────────

datasource:
url: jdbc:postgresql://localhost:5432/orbitview
username: orbituser
password: orbitpass
driver-class-name: org.postgresql.Driver
hikari:
maximum-pool-size: 20             # Max concurrent database connections
minimum-idle: 5                   # Min idle connections
connection-timeout: 30000         # Connection timeout (ms)
idle-timeout: 600000              # 10 minutes idle timeout
max-lifetime: 1800000             # 30 minutes max connection lifetime
auto-commit: true

# ─────────────────────────────────────────────────────────────────────────
# JPA/HIBERNATE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

jpa:
hibernate:
ddl-auto: update                  # auto | validate | create | create-drop | update
show-sql: false                     # Don't log SQL directly
open-in-view: false                 # Disable Open-In-View pattern
database-platform: org.hibernate.spatial.dialect.postgis.PostgisPG10Dialect
properties:
hibernate:
dialect: org.hibernate.spatial.dialect.postgis.PostgisPG10Dialect
format_sql: true                # Pretty-print SQL
jdbc:
batch_size: 20                # Batch insert/update size
fetch_size: 50                # Batch query fetch size
order_inserts: true             # Order bulk inserts for optimization
order_updates: true             # Order bulk updates for optimization
generate_statistics: false      # Disable statistics generation

# ─────────────────────────────────────────────────────────────────────────
# SECURITY (Keycloak OAuth2/OIDC)
# ─────────────────────────────────────────────────────────────────────────

security:
oauth2:
resourceserver:
jwt:
issuer-uri: http://localhost:8180/auth/realms/satellite-portal
jwk-set-uri: http://localhost:8180/auth/realms/satellite-portal/protocol/openid-connect/certs
jws-algorithm: RS256           # RSA SHA-256 algorithm

    # Basic Auth fallback (development only, use Keycloak in production)
    user:
      name: admin
      password: admin

# ─────────────────────────────────────────────────────────────────────────
# SERVLET MULTIPART FILE UPLOAD
# ─────────────────────────────────────────────────────────────────────────

servlet:
multipart:
max-file-size: 5GB                # Max single file size
max-request-size: 5GB             # Max total request size
location: /tmp/orbitview-uploads  # Temp upload directory
enabled: true

# ─────────────────────────────────────────────────────────────────────────
# JSON SERIALIZATION (Jackson)
# ─────────────────────────────────────────────────────────────────────────

jackson:
default-property-inclusion: non_null  # Exclude null fields from JSON
serialization:
indent-output: false              # Disable pretty-printing
deserialization:
fail-on-unknown-properties: false # Ignore unknown JSON fields

# ─────────────────────────────────────────────────────────────────────────
# WEB CORS CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

web:
cors:
allowed-origins: "http://localhost:3000,http://localhost:4200,http://localhost:8089"
allowed-methods: GET,POST,PUT,DELETE,OPTIONS,PATCH
allowed-headers: "*"
expose-headers: "Authorization,X-Correlation-ID,Content-Disposition"
allow-credentials: true
max-age: 3600                     # Cache preflight for 1 hour

# ─────────────────────────────────────────────────────────────────────────
# TASK EXECUTION (Async Processing)
# ─────────────────────────────────────────────────────────────────────────

task:
execution:
pool:
core-size: 3                    # Core thread pool size
max-size: 10                    # Max thread pool size
queue-capacity: 100             # Queue size before rejection
thread-name-prefix: image-processing-
rejection-policy: CALLER_RUNS   # Rejection policy
shutdown:
await-termination: true         # Wait for tasks to complete
await-termination-period: 60s   # Max wait time

    scheduling:
      pool:
        size: 2                         # Scheduled task threads
        thread-name-prefix: scheduled-

# ─────────────────────────────────────────────────────────────────────────
# RABBITMQ MESSAGE QUEUE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

rabbitmq:
# Connection Settings
host: localhost                     # RabbitMQ broker hostname
# Production: use ${RABBITMQ_HOST}
port: 5672                          # AMQP port (5671 for SSL)
username: guest                     # Change for production!
password: guest                     # Change for production!
virtual-host: /                     # RabbitMQ virtual host
connection-timeout: 10000           # Connection timeout (ms)

    # Publisher Settings (Message Confirmation)
    publisher-returns: true             # Enable return callback for unroutable messages
    publisher-confirm-type: correlated  # Confirm messages (SIMPLE | CORRELATED | NONE)

    # Listener Settings (Message Consumption)
    listener:
      simple:
        acknowledge-mode: manual        # Manual ack for better control (AUTO | MANUAL | NONE)
        prefetch: 1                     # Pre-fetch 1 message per worker
        retry:
          enabled: false                # Disable Spring AMQP retry (we handle manually)
        default-requeue-rejected: false  # Don't requeue failed messages automatically
        concurrency: 2               # Min-max concurrent workers (2-4 threads)
        max-concurrency: 4              # Max concurrent workers

    # Connection Pool Settings
    connection-pool:
      channels: 10                      # Channel pool size
      connection-limit: 10              # Max total connections


# ═══════════════════════════════════════════════════════════════════════════════
# MANAGEMENT (Actuator/Monitoring)
# ═══════════════════════════════════════════════════════════════════════════════

management:
endpoints:
web:
exposure:
include: "health,metrics,prometheus,info,env,configprops,loggers"
base-path: /actuator

endpoint:
health:
show-details: always              # Show detailed health info
show-components: always

metrics:
enabled: true
export:
prometheus:
enabled: true
step: 1m                        # Export metrics every minute


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

logging:
level:
root: INFO
com.Orbit_API: DEBUG                # Your application package
org.springframework: WARN
org.springframework.security: DEBUG
org.springframework.web: DEBUG
org.hibernate: WARN
org.hibernate.spatial: DEBUG
org.springframework.amqp: INFO      # RabbitMQ logging
org.springframework.rabbit: INFO

pattern:
console: "%d{yyyy-MM-dd HH:mm:ss} [%X{correlationId}] [%X{userId}] [%thread] %-5level %logger{36} - %msg%n"
file: "%d{yyyy-MM-dd HH:mm:ss} [%X{correlationId}] [%X{userId}] %-5level %logger{36} - %msg%n"

file:
name: logs/orbitview.log
max-size: 100MB
max-history: 30                     # Keep 30 days of logs
total-size-cap: 10GB


# ═══════════════════════════════════════════════════════════════════════════════
# MINIO CONFIGURATION (Object Storage)
# ═══════════════════════════════════════════════════════════════════════════════

minio:
url: http://localhost:9000
access-key: admin                     # Change in production!
secret-key: minioadmin                # Change in production!
bucket-raw: orbitview-raw-images      # Original satellite images
bucket-cog: orbitview-processed-cogs  # Cloud-Optimized GeoTIFFs
bucket-thumb: orbitview-thumbnails    # Image thumbnails
bucket-previews: orbitview-previews   # Preview images
use-ssl: false                        # Enable SSL in production
region: us-east-1
bucket-exports: orbitview-exports     # Export/download packages

upload:
chunk-size: 5242880                 # 5MB chunks for multipart uploads
retry-attempts: 3
retry-delay-ms: 1000


# ═══════════════════════════════════════════════════════════════════════════════
# GEOSERVER CONFIGURATION (Map Tile Server)
# ═══════════════════════════════════════════════════════════════════════════════

geoserver:
url: http://localhost:8081/geoserver
base-url: http://localhost:8081/geoserver
rest-url: http://localhost:8081/geoserver/rest
username: admin
password: geoserver                   # Change in production!
workspace: satellite-portal

publish:
retry-attempts: 3
retry-delay-ms: 2000
verify-layer: true                  # Verify layer after publishing

timeout:
connect-ms: 10000
read-ms: 30000
write-ms: 30000


# ═══════════════════════════════════════════════════════════════════════════════
# KEYCLOAK CONFIGURATION (OAuth2/OIDC Authentication)
# ═══════════════════════════════════════════════════════════════════════════════

keycloak:
realm: satellite-portal
auth-server-url: http://localhost:8180/auth
ssl-required: external                # external | none | all
resource: satellite-portal-api        # Client ID
bearer-only: true                     # Only bearer tokens (not web app)
realm.public-key: ${KEYCLOAK_PUBLIC_KEY:}  # Set via environment variable
verify-token-aud: false
credentials:
secret: ${KEYCLOAK_CLIENT_SECRET:}


# ═══════════════════════════════════════════════════════════════════════════════
# RESILIENCE4J CONFIGURATION (Retry & Circuit Breaker - Fault Tolerance)
# ═══════════════════════════════════════════════════════════════════════════════

resilience4j:

# ─────────────────────────────────────────────────────────────────────────
# Retry Configuration for External Services
# ─────────────────────────────────────────────────────────────────────────

retry:
instances:
# GeoServer Publishing Retry
geoserver-publish:
max-attempts: 3
wait-duration: 5000             # 5 seconds between retries
retry-exceptions:
- org.springframework.web.client.RestClientException
- java.io.IOException
ignore-exceptions:
- java.lang.NullPointerException

      # MinIO Upload Retry with Exponential Backoff
      minio-upload:
        max-attempts: 3
        wait-duration: 2000
        exponential-backoff:
          multiplier: 2                 # Double wait each retry
          initial-interval: 1000        # Start with 1 second
          max-interval: 60000           # Cap at 60 seconds

# ─────────────────────────────────────────────────────────────────────────
# Circuit Breaker Configuration for External Services
# ─────────────────────────────────────────────────────────────────────────

circuitbreaker:
instances:
# GeoServer Circuit Breaker
geoserver:
register-health-indicator: true
failure-rate-threshold: 50      # 50% failures = open circuit
slow-call-rate-threshold: 50    # 50% slow calls = open circuit
slow-call-duration-threshold: 30000  # 30 seconds = slow
permitted-number-of-calls-in-half-open-state: 3
automatic-transition-from-open-to-half-open-enabled: true
wait-duration-in-open-state: 60000  # 60 seconds before retry
record-exceptions:
- org.springframework.web.client.RestClientException
- java.io.IOException

      # MinIO Circuit Breaker
      minio:
        register-health-indicator: true
        failure-rate-threshold: 60      # 60% failures = open
        slow-call-rate-threshold: 50
        slow-call-duration-threshold: 20000  # 20 seconds = slow
        permitted-number-of-calls-in-half-open-state: 5
        wait-duration-in-open-state: 30000   # 30 seconds before retry

# ─────────────────────────────────────────────────────────────────────────
# Bulkhead Configuration (Concurrency Control)
# ─────────────────────────────────────────────────────────────────────────

bulkhead:
instances:
image-processing:
max-concurrent-calls: 10        # Max 10 concurrent calls
max-wait-duration: 10000        # Wait up to 10 seconds
wait-duration-in-open-state: 5000


# ═══════════════════════════════════════════════════════════════════════════════
# MICROMETER METRICS
# ═══════════════════════════════════════════════════════════════════════════════

metrics:
export:
prometheus:
enabled: true
step: 1m                          # Export metrics every minute


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM ORBITVIEW APPLICATION PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

orbitview:
shared-data-dir: /tmp/orbitview-shared

# ─────────────────────────────────────────────────────────────────────────
# Image Processing Configuration
# ─────────────────────────────────────────────────────────────────────────

processing:
gdal-timeout-minutes: 30            # Max GDAL process runtime
temp-dir: /tmp/orbitview-temp       # Temporary processing directory

# ─────────────────────────────────────────────────────────────────────────
# Storage Configuration
# ─────────────────────────────────────────────────────────────────────────

storage:
enable-multipart: true              # Enable multipart uploads
chunk-size-mb: 5                    # Chunk size for uploads

# ─────────────────────────────────────────────────────────────────────────
# REST API Configuration
# ─────────────────────────────────────────────────────────────────────────

api:
version: v1
base-path: /api/v1                  # REST API base path

# ─────────────────────────────────────────────────────────────────────────
# RABBITMQ MESSAGE QUEUE CONFIGURATION (OrbitView-specific)
# ─────────────────────────────────────────────────────────────────────────

rabbitmq:
# Exchange Configuration
exchange: orbitview.images          # Main message exchange
exchange-type: direct               # Exchange type: direct, fanout, or topic

    # Image Ingest Queue (Main Processing Queue)
    ingest-queue: orbitview.image.ingest
    ingest-routing-key: image.ingest

    # Retry Queue (Failed messages retry here after TTL)
    retry-queue: orbitview.image.ingest.retry
    retry-routing-key: image.ingest.retry
    retry-ttl-ms: 30000                 # 30 seconds between retries

    # Dead Letter Queue (Permanently failed messages)
    dlq-queue: orbitview.image.ingest.dlq
    dlq-routing-key: image.ingest.dlq
    dlq-exchange: orbitview.images.dlx  # Dead Letter eXchange

    # Consumer Settings
    prefetch-count: 1                   # Messages to prefetch per worker
    concurrency: 2                      # Number of concurrent workers
    # Increase for more throughput (2-10)
    max-retries: 3                      # Max retry attempts before DLQ


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM APP PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════════

app:
name: OrbitView
version: 1.0.0
description: Satellite Image Intelligence Portal

cors:
allowed-origins: "http://localhost:3000,http://localhost:4200"
allowed-methods: GET,POST,PUT,DELETE,OPTIONS,PATCH
allow-credentials: true
max-age: 3600

security:
jwt:
expiration-minutes: 30
refresh-expiration-days: 7
cors:
expose-headers: "Authorization,X-Correlation-ID"

file-upload:
max-size-mb: 5120                   # 5GB
allowed-extensions: "tif,tiff,geotiff,jp2,jpeg2000,nitf,ntf,env,bil"
temp-directory: /tmp/orbitview-uploads


# ═══════════════════════════════════════════════════════════════════════════════
# FEIGN CLIENT CONFIGURATION (External API Calls)
# ═══════════════════════════════════════════════════════════════════════════════

feign:
httpclient:
enabled: true
connection-timeout: 10000
max-connections: 100
max-connections-per-route: 10


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT-SPECIFIC PROFILES
# =================================================================================================================================================================================================================================================================

---

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE: DEVELOPMENT (Local Development)
# ═══════════════════════════════════════════════════════════════════════════════

spring:
config:
activate:
on-profile: dev

server:
port: 8089

logging:
level:
root: INFO
com.Orbit_API: DEBUG
org.springframework: WARN
org.springframework.amqp: INFO
org.springframework.rabbit: INFO


---

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE: PRODUCTION (Production Deployment)
# ═══════════════════════════════════════════════════════════════════════════════
#
#spring:
#  datasource:
#    url: jdbc:postgresql://prod-db.example.com:5432/orbitview-prod
#    username: ${DB_USERNAME}            # Environment variable
#    password: ${DB_PASSWORD}            # Environment variable
#  config:
#    activate:
#      on-profile: prod
#
#server:
#  port: 8080
#  ssl:
#    enabled: false                      # Use reverse proxy (Nginx) for SSL
#
##spring:
##  datasource:
##    url: jdbc:postgresql://prod-db.example.com:5432/orbitview-prod
##    username: ${DB_USERNAME}            # Environment variable
##    password: ${DB_PASSWORD}            # Environment variable
#
#  jpa:
#    hibernate:
#      ddl-auto: validate                # Validate only, never modify schema
#
#  rabbitmq:
#    host: ${RABBITMQ_HOST}              # Environment variable
#    port: 5672
#    username: ${RABBITMQ_USER}
#    password: ${RABBITMQ_PASSWORD}
#    ssl: true                           # Enable SSL for RabbitMQ
#    virtual-host: /
#
#logging:
#  level:
#    root: WARN
#    com.Orbit_API: INFO
#    org.springframework: WARN
#    org.springframework.amqp: INFO
#

---

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE: STAGING (Pre-Production Testing)
# ═══════════════════════════════════════════════════════════════════════════════

#spring:
#  config:
#    activate:
#      on-profile: staging
#
#server:
#  port: 8080
#  ssl:
#    enabled: true
#    key-store: /path/to/keystore.jks
#    key-store-password: ${SSL_KEYSTORE_PASSWORD}
#
#spring:
#  datasource:
#    url: jdbc:postgresql://staging-db.example.com:5432/orbitview-staging
#    username: ${DB_USERNAME}
#    password: ${DB_PASSWORD}
#
#  rabbitmq:
#    host: ${RABBITMQ_HOST}
#    port: 5672
#    username: ${RABBITMQ_USER}
#    password: ${RABBITMQ_PASSWORD}
#
#logging:
#  level:
#    root: INFO
#    com.Orbit_API: DEBUG
#    org.springframework: WARN
#

---

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE: TESTING (Unit/Integration Tests)
# ═══════════════════════════════════════════════════════════════════════════════

#spring:
#  config:
#    activate:
#      on-profile: test
#
#server:
#  port: 0                               # Random port for parallel tests
#
#spring:
#  datasource:
#    url: jdbc:h2:mem:testdb             # In-memory H2 database
#    username: sa
#    password: sa
#    driver-class-name: org.h2.Driver
#
#  jpa:
#    database-platform: org.hibernate.dialect.H2Dialect
#    hibernate:
#      ddl-auto: create-drop             # Create and drop for each test
#
#  rabbitmq:
#    host: localhost
#    port: 5672
#
#logging:
#  level:
#    root: WARN
#    com.Orbit_API: DEBUG



#### src/main/resources/logback.xml
---
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%X{correlationId}] [%X{userId}] [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/orbitview.log</file>
        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%X{correlationId}] [%X{userId}] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/orbitview-%d{yyyy-MM-dd}-%i.log</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>

    <logger name="com.Orbit_API" level="DEBUG"/>
    <logger name="org.springframework" level="WARN"/>

    <root level="INFO">
        <appender-ref ref="STDOUT"/>
        <appender-ref ref="FILE"/>  
    </root>
</configuration>
---


