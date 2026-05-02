package com.aliya.fetchjobapp.job;

import jakarta.persistence.Entity;

import java.math.BigDecimal;

@Entity
public class Job {

    private Long id;

    private String title;

    private String description;

    private String location;

    private String status;

    private BigDecimal minSalary;

    private BigDecimal maxSalary;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public BigDecimal getMinSalary() {
        return minSalary;
    }

    public void setMinSalary(BigDecimal minSalary) {
        this.minSalary = minSalary;
    }

    public BigDecimal getMaxSalary() {
        return maxSalary;
    }

    public void setMaxSalary(BigDecimal maxSalary) {
        this.maxSalary = maxSalary;
    }

    public Job(long id, String title, String description, String location, String status, BigDecimal minSalary, BigDecimal maxSalary) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.status = status;
        this.location = location;
        this.minSalary = minSalary;
        this.maxSalary = maxSalary;
    }
}
