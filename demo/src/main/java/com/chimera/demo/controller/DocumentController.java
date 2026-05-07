package com.chimera.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.chimera.demo.model.Document;
import com.chimera.demo.repository.DocumentRepository;

import jakarta.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/api/documents")
public class DocumentController {

    @Autowired
    private DocumentRepository documentRepository;

    // ❌ VULNERÁVEL: qualquer usuário acessa qualquer documento pelo ID
    @GetMapping("/{id}")
    public ResponseEntity<Document> getDocument(
        @PathVariable Long id,
        HttpServletRequest request
    ) {
        Long authenticatedUserId = (Long) request.getAttribute("authenticatedUserId");
        String role =  SecurityContextHolder.getContext()
                .getAuthentication()
                .getAuthorities()
                .stream()
                .findFirst()
                .map(a -> a.getAuthority()) // retorna "ROLE_ADMIN" ou "ROLE_USER"
                .orElse("");

        return documentRepository.findById(id)
            .filter(doc ->
                doc.getOwnerId().equals(authenticatedUserId) || role.equals("ROLE_ADMIN")
            )
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.status(403).build()); // 403 e não 404!
    }

    // ❌ VULNERÁVEL: qualquer usuário deleta qualquer documento
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDocument(@PathVariable Long id) {
        documentRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}