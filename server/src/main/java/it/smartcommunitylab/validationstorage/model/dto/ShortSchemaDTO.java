package it.smartcommunitylab.validationstorage.model.dto;

import java.io.Serializable;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;

import it.smartcommunitylab.validationstorage.common.ValidationStorageUtils;
import lombok.Data;

/**
 * Request object: schema of the data.
 */
@Data
@Valid
public class ShortSchemaDTO {
    /**
     * ID of the experiment this document belongs to.
     */
    @NotBlank
    @Pattern(regexp = ValidationStorageUtils.ID_PATTERN)
    private String experimentId;

    /**
     * Name of the experiment this document belongs to.
     */
    @Pattern(regexp = ValidationStorageUtils.NAME_PATTERN)
    private String experimentName;

    /**
     * ID of the run this document belongs to.
     */
    @NotBlank
    @Pattern(regexp = ValidationStorageUtils.ID_PATTERN)
    private String runId;

    /**
     * May contain extra information.
     */
    private Map<String, Serializable> contents;
}