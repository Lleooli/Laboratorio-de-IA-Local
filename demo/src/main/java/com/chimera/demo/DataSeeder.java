/*package com.chimera.demo;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.chimera.demo.model.Document;
import com.chimera.demo.model.User;
import com.chimera.demo.repository.DocumentRepository;
import com.chimera.demo.repository.UserRepository;

@Component
public class DataSeeder implements CommandLineRunner {

    @Autowired UserRepository userRepo;
    @Autowired DocumentRepository docRepo;

    @Override
    public void run(String... args) {
        User alice = new User(); alice.setUsername("alice"); alice.setRole("user");
        User bob   = new User(); bob.setUsername("bob");   bob.setRole("user");
        userRepo.saveAll(List.of(alice, bob));

        Document d1 = new Document();
        d1.setTitle("Contrato Confidencial"); d1.setContent("Dados sensíveis da Alice");
        d1.setOwnerId(alice.getId());

        Document d2 = new Document();
        d2.setTitle("Relatório Interno"); d2.setContent("Dados sensíveis do Bob");
        d2.setOwnerId(bob.getId());

        docRepo.saveAll(List.of(d1, d2));
    }
}
*/