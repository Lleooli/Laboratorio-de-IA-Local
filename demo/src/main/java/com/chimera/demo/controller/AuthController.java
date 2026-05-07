package com.chimera.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.chimera.demo.dto.LoginRequest;
import com.chimera.demo.dto.LoginResponse;
import com.chimera.demo.repository.UserRepository;
import com.chimera.demo.security.JwtUtil;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;

    public AuthController(UserRepository userRepository, JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        // Busca por username (adapte para usar senha com BCrypt em produção)
        return userRepository.findByUsername(request.username())
            .map(user -> {
                String token = jwtUtil.generateToken(
                    user.getUsername(), user.getRole(), user.getId()
                );
                return ResponseEntity.ok(
                    new LoginResponse(token, user.getUsername(), user.getRole())
                );
            })
            .orElse(ResponseEntity.status(401).build());
    }
}