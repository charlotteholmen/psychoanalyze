// Command pyramid-watcher rebuilds docs/architecture-diagrams/testing-pyramid.d2
// from Gherkin feature files in tests/features/.
//
// It parses @tier: tags and Scenario names via the official Cucumber Gherkin
// parser, then constructs the D2 diagram using the d2oracle API for type-safe,
// validated diagram generation.
//
// Usage:
//
//	pyramid-watcher                  # one-shot rebuild
//	pyramid-watcher --watch          # watch & rebuild on change
package main

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"

	gherkin "github.com/cucumber/gherkin/go/v28"
	messages "github.com/cucumber/messages/go/v24"
	"github.com/fsnotify/fsnotify"

	"oss.terrastruct.com/d2/d2format"
	"oss.terrastruct.com/d2/d2lib"
	"oss.terrastruct.com/d2/d2oracle"
	dlog "oss.terrastruct.com/d2/lib/log"
)

// ---------------------------------------------------------------------------
// Tier metadata
// ---------------------------------------------------------------------------

type tierMeta struct {
	key      string
	label    string
	varName  string
	fill     string
	stroke   string
	itemFill string
}

var tierOrder = []tierMeta{
	{
		key: "e2e", label: "E2E / UI", varName: "e2e_tier",
		fill: "#ffebee", stroke: "#c62828", itemFill: "#fff5f5",
	},
	{
		key: "integration", label: "Integration", varName: "integration_tier",
		fill: "#e3f2fd", stroke: "#1565c0", itemFill: "#e8f0fe",
	},
	{
		key: "domain", label: "Domain / Contract", varName: "domain_tier",
		fill: "#e8f5e9", stroke: "#2e7d32", itemFill: "#f1f8e9",
	},
}

// ---------------------------------------------------------------------------
// Parsed feature
// ---------------------------------------------------------------------------

type featureSpec struct {
	stem      string
	filename  string
	tier      string
	scenarios []string
}

var tierTagRe = regexp.MustCompile(`@tier:(\w+)`)

func d2ID(stem string) string {
	return strings.ReplaceAll(stem, "-", "_")
}

// ---------------------------------------------------------------------------
// Gherkin parsing (official Cucumber parser)
// ---------------------------------------------------------------------------

func parseFeatureFile(path string) (*featureSpec, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	uuid := &messages.UUID{}
	doc, err := gherkin.ParseGherkinDocument(f, uuid.NewId)
	if err != nil {
		return nil, fmt.Errorf("gherkin parse %s: %w", path, err)
	}
	if doc.Feature == nil {
		return nil, nil
	}

	// Extract @tier: from feature-level tags
	var tier string
	for _, tag := range doc.Feature.Tags {
		if m := tierTagRe.FindStringSubmatch(tag.Name); m != nil {
			tier = m[1]
			break
		}
	}
	if tier == "" {
		return nil, nil // skip features without a @tier: tag
	}

	// Collect scenario names
	var scenarios []string
	for _, child := range doc.Feature.Children {
		if child.Scenario != nil {
			scenarios = append(scenarios, child.Scenario.Name)
		}
	}

	base := filepath.Base(path)
	stem := strings.TrimSuffix(base, filepath.Ext(base))

	return &featureSpec{
		stem:      stem,
		filename:  base,
		tier:      tier,
		scenarios: scenarios,
	}, nil
}

func parseAllFeatures(dir string) ([]featureSpec, error) {
	entries, err := filepath.Glob(filepath.Join(dir, "*.feature"))
	if err != nil {
		return nil, err
	}
	sort.Strings(entries)

	var features []featureSpec
	for _, path := range entries {
		spec, err := parseFeatureFile(path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "warning: %v\n", err)
			continue
		}
		if spec != nil {
			features = append(features, *spec)
		}
	}
	return features, nil
}

// ---------------------------------------------------------------------------
// D2 diagram construction via d2oracle
// ---------------------------------------------------------------------------

func buildDiagram(features []featureSpec) (string, error) {
	ctx := dlog.WithDefault(context.Background())

	// Start with an empty compiled graph
	_, graph, err := d2lib.Compile(ctx, "", nil, nil)
	if err != nil {
		return "", fmt.Errorf("d2 compile empty: %w", err)
	}

	// Helper: set a string attribute on the graph
	set := func(key, val string) error {
		g, setErr := d2oracle.Set(graph, nil, key, nil, &val)
		if setErr != nil {
			return fmt.Errorf("set %s=%s: %w", key, val, setErr)
		}
		graph = g
		return nil
	}

	// Helper: create a shape/edge
	create := func(key string) error {
		g, _, createErr := d2oracle.Create(graph, nil, key)
		if createErr != nil {
			return fmt.Errorf("create %s: %w", key, createErr)
		}
		graph = g
		return nil
	}

	// -- title --
	if err := create("title"); err != nil {
		return "", err
	}
	if err := set("title", "Testing Pyramid — tests/features/"); err != nil {
		return "", err
	}
	if err := set("title.shape", "text"); err != nil {
		return "", err
	}
	if err := set("title.near", "top-center"); err != nil {
		return "", err
	}
	if err := set("title.style.font-size", "22"); err != nil {
		return "", err
	}
	if err := set("title.style.bold", "true"); err != nil {
		return "", err
	}

	// Group features by tier
	tiers := make(map[string][]featureSpec)
	for _, f := range features {
		tiers[f.tier] = append(tiers[f.tier], f)
	}
	for _, fs := range tiers {
		sort.Slice(fs, func(i, j int) bool { return fs[i].filename < fs[j].filename })
	}

	// Create tier containers, features, and scenario labels
	for _, tm := range tierOrder {
		v := tm.varName

		if err := create(v); err != nil {
			return "", err
		}
		if err := set(v, tm.label); err != nil {
			return "", err
		}
		if err := set(v+".shape", "parallelogram"); err != nil {
			return "", err
		}
		if err := set(v+".style.fill", tm.fill); err != nil {
			return "", err
		}
		if err := set(v+".style.stroke", tm.stroke); err != nil {
			return "", err
		}
		if err := set(v+".style.stroke-width", "2"); err != nil {
			return "", err
		}

		for _, feat := range tiers[tm.key] {
			fid := fmt.Sprintf("%s.%s", v, d2ID(feat.stem))

			if err := create(fid); err != nil {
				return "", err
			}
			if err := set(fid, feat.filename); err != nil {
				return "", err
			}
			if err := set(fid+".style.fill", tm.itemFill); err != nil {
				return "", err
			}

			for i, scenario := range feat.scenarios {
				sid := fmt.Sprintf("%s.s%d", fid, i+1)
				if err := create(sid); err != nil {
					return "", err
				}
				if err := set(sid, scenario); err != nil {
					return "", err
				}
			}
		}
	}

	// Pyramid edges: domain_tier -> integration_tier -> e2e_tier
	for i := len(tierOrder) - 1; i > 0; i-- {
		edgeKey := fmt.Sprintf("%s -> %s", tierOrder[i].varName, tierOrder[i-1].varName)
		if err := create(edgeKey); err != nil {
			return "", err
		}
	}

	return d2format.Format(graph.AST), nil
}

// ---------------------------------------------------------------------------
// Rebuild
// ---------------------------------------------------------------------------

func rebuild(featuresDir, outputPath string) error {
	features, err := parseAllFeatures(featuresDir)
	if err != nil {
		return err
	}

	script, err := buildDiagram(features)
	if err != nil {
		return err
	}

	header := "# Testing pyramid — auto-generated from tests/features/\n" +
		"# Do not edit by hand; run tools/pyramid-watcher\n\n"

	if err := os.WriteFile(outputPath, []byte(header+script), 0644); err != nil {
		return err
	}

	totalScenarios := 0
	for _, f := range features {
		totalScenarios += len(f.scenarios)
	}
	fmt.Printf("  wrote %s  (%d features, %d scenarios)\n", outputPath, len(features), totalScenarios)
	return nil
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

func main() {
	root, err := findRepoRoot()
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}

	featuresDir := filepath.Join(root, "tests", "features")
	outputPath := filepath.Join(root, "docs", "architecture-diagrams", "testing-pyramid.d2")

	if err := rebuild(featuresDir, outputPath); err != nil {
		fmt.Fprintf(os.Stderr, "rebuild failed: %v\n", err)
		os.Exit(1)
	}

	if !hasFlag("--watch") {
		return
	}

	// --- Watch mode (fsnotify) ---
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		fmt.Fprintf(os.Stderr, "watcher: %v\n", err)
		os.Exit(1)
	}
	defer watcher.Close()

	if err := watcher.Add(featuresDir); err != nil {
		fmt.Fprintf(os.Stderr, "watch %s: %v\n", featuresDir, err)
		os.Exit(1)
	}
	fmt.Printf("  watching %s for changes (Ctrl+C to stop) ...\n", featuresDir)

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			if event.Op&(fsnotify.Write|fsnotify.Create|fsnotify.Remove|fsnotify.Rename) != 0 {
				fmt.Printf("  changed: %s\n", filepath.Base(event.Name))
				if err := rebuild(featuresDir, outputPath); err != nil {
					fmt.Fprintf(os.Stderr, "rebuild error: %v\n", err)
				}
			}
		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			fmt.Fprintf(os.Stderr, "watcher error: %v\n", err)
		}
	}
}

func hasFlag(flag string) bool {
	for _, arg := range os.Args[1:] {
		if arg == flag {
			return true
		}
	}
	return false
}

func findRepoRoot() (string, error) {
	dir, err := os.Getwd()
	if err != nil {
		return "", err
	}
	for {
		if _, err := os.Stat(filepath.Join(dir, "pyproject.toml")); err == nil {
			return dir, nil
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			return "", fmt.Errorf("could not find repo root (looked for pyproject.toml)")
		}
		dir = parent
	}
}
